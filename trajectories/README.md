# trajectories/

跑批后的轨迹与账本归档处。目录约定：

```
trajectories/
  T_run1/  T_run2/  T_run3/     # 语义检索平铺条件
  G_run1/  G_run2/  G_run3/     # 编排图指导条件
  参照_B0/                      # v1 Plan1 + v2 冒烟的口径补算笔记（不重跑）
```

每个 run 目录至少含：`ledger/{graph.yaml,hypotheses.json,costs.json,stages.json}` + `trajectory_steps.jsonl`（或 timeline）+ 结束快照（git status/diff --stat、artifact 清单、eval_report）。

参照轨迹原件在 `autotune轨迹分析/输入材料/{v1,v2}/`（不入本仓库，体积大）。
