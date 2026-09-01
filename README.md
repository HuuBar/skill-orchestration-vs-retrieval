# skill 编排图 vs 语义检索 · 对比实验工作区

**问题**：skill 多层图（编排结构）相对传统语义检索平铺，在真实 ML 优化任务上带来多少增量？
**论点**（待检验）：skill 文本授予动机，图结构授予纪律——T→G 的差值 = 编排结构的贡献。

## 结构

```
docs/
  实验方案_v3.md          # 条件定义/任务轮次/指标/判定规则（先读这个）
  git分支探查bug_诊断.md   # v2 冒烟唯一 trial 死因诊断 + H4 第四错误类建议（跑批前必读）
conditions/
  T_语义检索平铺/config.md  # T 条件：平铺+检索，图开关关闭
  G_编排图指导/            # G 条件：离线模拟编排产出
    graph_tbox.yaml       #   编排图（7 节点 + requires/informs/no_parallel + 验证门 + 禁改区）
    metaplan_view.md      #   meta-plan 视图模板（每轮现渲染 ≤2000 字符）
skills/                   # 16 个任务对口 skill（待从 skillnet 导出放入，两边用同一批）
analysis/
  compare_trajectories.py # 事后指标计算：python3 compare_trajectories.py T_run1 G_run1
trajectories/             # 跑批归档（目录约定见内）
```

## 跑批前置（阻塞项）

1. **修 git 分支探查 bug**（`docs/git分支探查bug_诊断.md`），并用同一 tbox 目标 `max_trials≥3` 验证通过；
2. 建议落地 **harness_fault 第四错误类**（框架病不落负证据、不计 attempts）——否则框架 bug 会污染假说账本，实验数据失真；
3. 16 个 skill 文件放入 `skills/`。

## 与正式评测的关系

本仓库是**方向性 pilot**（T/G 各 3 次真实任务 run）。正式评测设计（任务分层/统计检验/样本量）见《skill多层图_vs_skill搜集_评测交接报告》，pilot 判定"是否值得上正式评测"。
