# git 分支探查 bug 诊断（v2 冒烟 run-20260831-080946 唯一 trial 死因）

> 来源：v2 轨迹（`autotune轨迹分析/输入材料/v2/`）。本诊断基于轨迹原文，修复落在真实代码库后按 §4 验证。

## 1. 症状

trial h1 在执行阶段死亡，Debugger 诊断轨迹（`trajectory_timeline.md` step19-44）显示：

```
git checkout h1-Plan1-特征扩展-超参调优-验证集阈值校准-
error: pathspec '...' did not match any file(s) known to git
```

- 分支名**尾部多一个连字符**（`...校准-`）；
- 仓库里只有 `master` 一个 ref——目标分支根本不存在；
- safe_bash 白名单拦截了诊断用的 `git branch` 命令（Debugger 只能只读勘察，无法直接验证分支列表）。

## 2. 根因假设（按可能性排序）

1. **建名/用名两条 slug 路径不一致**：plan 标题 `Plan1 - 特征扩展 + 超参调优 + 验证集阈值校准 双指标优化` 含 CJK 与 `+` 分隔符。若建分支时的 slug 与 checkout 时的 slug 不是同一个函数（或同一函数但输入不同——如一个带序号后缀一个不带），CJK 剥离/截断后就会产生尾部 `-` 的差异，create 用名 ≠ checkout 用名。
2. **建分支静默失败**：create 失败被吞（未检查返回码），checkout 前又不验证分支存在。
3. **截断位置不当**：分支名有长度限制，按字符截断后正好停在分隔符上，未 strip 尾部 `-_./`。

## 3. 修复模式（建议）

- **单一 slug 函数**：分支名的生成收敛到一个函数 `slugify_branch(node_id, title)`，create/checkout/删除全部经它，禁止第二处拼名；
- slug 规则：小写化 → 非 `[a-z0-9]` 一律转 `-` → 折叠连续 `-` → **strip 首尾 `-`** → 截断到 48 字符后再 strip 一次；
- create 后立即 `git rev-parse --verify` 验证存在，失败即抛（不要静默吞掉）；
- checkout 前 `git branch --list` 校验，缺失时报 harness 自身故障而不是继续往下走。

## 4. 验证

修好后用同一 tbox 目标跑 `max_trials≥3`：要求每个 trial 的分支 create→checkout→diff export 全程无 pathspec 错误；ledger 中节点能走到 done 或真实的 failed_*（而不是被框架 bug 杀死）。

## 5. 更重要的发现：这个 bug 暴露了 H4 三分类的盲区

轨迹里该失败被 `default_permanent` 裁决为 permanent，并给 h1 落了**负证据**（`hypotheses.json` verdict=negative，理由"配置不可行=信息"）。

**这是错记**：假说没有做错任何事——是 harness 的分支管理代码自己的病。负证据会喂回调度（E9 降权、投影告知 planner"此路不通"），等于框架的病被记成假说的罪，静默带偏后续探索方向。

**处置建议**（H4 增补第四类或特判）：

| 类 | 判定 | 处置 |
|---|---|---|
| harness_fault（新增） | 异常来自框架自身代码路径（分支管理/账本/调度），非试验内容 | **不落负证据、不计 attempts**；节点 →failed_transient 重排或 frozen 待修；修 bug 后该假说应能干净重跑 |

判别启发式：异常栈/消息落在 orchestration 层（git/checkout/ledger 写入）而非 trial 的 prepare/execute/evaluate 业务路径。这条应同步进 05 总纲 §6 H4 交接卡与错误分类规则表。
