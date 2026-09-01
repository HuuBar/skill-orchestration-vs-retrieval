# 改动任务卡（执行 agent 专用，自包含）

> 你要对 `/home/z50061485/autotune-harness` 做**恰好三处改动**，不多不少。
> 完整背景见同目录《放置与代码改动清单.md》《执行手册.md》；本卡自足，照做即可。
> 每处改动带验收检查，**三个检查全过才能开始跑批**。

## 改动 1【必修】git 分支名 bug 修复

**症状**（来自 run-20260831-080946 轨迹）：trial 死于 `git checkout h1-Plan1-特征扩展-超参调优-验证集阈值校准-`——分支名尾部多连字符、分支不存在，pathspec 报错。

**定位**：在编排层找分支名构造点：
```bash
grep -rn "checkout" /home/z50061485/autotune-harness/src/ /home/z50061485/autotune-harness/.opencode/ 2>/dev/null
grep -rn "branch" /home/z50061485/autotune-harness/src/ | grep -i "create\|format\|slug\|name"
```

**改法**：分支名生成收敛为单一函数，create/checkout 共用它；建后立即验证。可直接贴入（`放置与代码改动清单.md` §B-1 有完整注释版）：

```python
import re, subprocess

def slugify_branch(node_id: str, title: str) -> str:
    s = f"{node_id}-{title}".lower()
    s = re.sub(r"[^a-z0-9一-鿿]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-_.")
    return s[:48].strip("-_.")

def ensure_branch(repo: str, name: str, base: str = "master") -> None:
    if not subprocess.run(["git", "-C", repo, "branch", "--list", name],
                          capture_output=True, text=True).stdout.strip():
        subprocess.run(["git", "-C", repo, "checkout", "-b", name, base], check=True)
    subprocess.run(["git", "-C", repo, "rev-parse", "--verify", name], check=True)
```

**验收**：CJK 标题建分支首尾无 `-`，`git rev-parse --verify` 通过；冒烟 run 的 trial 不再死于 pathspec。

## 改动 2【T 条件】注册 skill_search 工具

**改法**：把 `skill-orchestration-vs-retrieval/dist/T/skill_search.py` 放进 harness 的工具模块，按你们既有工具的同款方式注册为 `skill_search`。设置环境变量 `SKILLS_FLAT_DIR=/home/z50061485/autotune-harness/skills_flat`。

**验收**：agent 工具列表出现 skill_search；试调 `skill_search("数据清洗 重复列")` 返回 data-cleaning-pipeline-generator 等结果。

## 改动 3【G 条件】离线图注入入口

**先查**：KnowledgeGraphMiddleware 的配置是否已支持图文件输入。
- **支持** → 零改码，G 的 config 里指向 `/home/z50061485/skill-orchestration-vs-retrieval/dist/G/graph_tbox.yaml`；
- **只支持在线编译** → 在 run 初始化的编图调用前加旁路：

```python
if cfg.get("init_graph_path"):           # 离线预编图直接作为初始状态
    shutil.copy(cfg["init_graph_path"], run_dir / "ledger" / "graph.yaml")
else:
    compile_graph_online(...)            # 原路径不动
```

**字段映射**：把 graph_tbox.yaml 的键名按中间件实际 schema 机械映射（nodes/edges/verify 等，只改键名不改语义）。**映射后的版本 commit 回实验仓库，并发给郑哲宁过目**——这是唯一需要回头的点。

**验收**：G 冒烟 run 中，Planner 的 system message 里出现 meta-plan 视图，结构对照 `dist/G/metaplan_view.md`。

## 两个条件的 config 对照（改完代码后配）

| 配置项 | T | G |
|---|---|---|
| knowledge_graph.enabled | false | true |
| init_graph_path（或 source） | — | graph_tbox.yaml 绝对路径 |
| skill_search 工具 | 注册 | 不注册 |
| max_trials / 模型 / 温度 / 白名单 / 任务书 | 两边逐字一致 | 同左 |

## 不许动的（防止顺手施工）

prompt/agent.md、四个 agent 实现、状态机词表边表、账本结构、安全点、scheduler 的 requires/no_parallel/informs 语义、错误分类器（harness_fault 不施工，分析期标记处理）、tbox 项目本体。

## 改完后的顺序

三个验收全过 → 按《执行手册.md》Step 4 双冒烟 → Step 5 交替跑批（T1→G1→T2→G2→T3→G3）→ 归档 trajectories/ → 联系郑哲宁出对照分析。
