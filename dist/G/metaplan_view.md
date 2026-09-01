# meta-plan 视图模板（G 条件 · 每轮现渲染，≤2000 字符）

> 渲染规则：每次 Planner 模型调用时从 graph.yaml + hypotheses 账本现算注入 system message，不依赖历史消息（免疫摘要压缩）。占位符 `{...}` 由 ViewBuilder 填充。

```
【meta-plan · run {run_id} · 第 {round} 轮】
目标：recall≥0.70 前提下 neg_recall 0.457→0.65+（f1 越高越好）
硬约束：阈值只在 val 选（禁 test）；val<500 样本升 K 折；提升<噪声带宽=不显著；
        禁改区：评测代码/test 标签/split_manifest/data/

图状态（后验排序）：
{nodes_table}
  示例行：A4_feature     ready    posterior=0.62  待做：特征扩展+零重要度清理
          A6_threshold   locked   ←requires A5_train；与 A4 互斥（单原子变更）

已验证事实：{verified_facts}        # 证据账本里的阳性结论
负证据（此路不通）：{negative_evidence}  # 含原因；提议前先看这里，别重复提议死方向
待决决策点：{open_decisions}         # 需要你判断的开放点
冲突提示：{no_parallel_holds}        # 当前被扣留的节点及原因

你的自由度：可以提议图外新假说（走正常裁决）；优先级判断归你。
```

## 与 T 条件的本质区别（"指导 vs 注入"自查表）

| 维度 | 本视图（G） | skill 检索（T） |
|---|---|---|
| 时效 | 每轮现渲染，随账本变化 | 检索那一刻的静态文本 |
| 抗压缩 | 注入 system message，免疫历史摘要 | 检索结果在历史消息里，会被压缩掉 |
| 顺序保证 | requires/no_parallel 由 scheduler 查表执行 | skill 文本里的"建议顺序"靠模型自觉 |
| 负证据 | 显式列出、每轮可见 | 无此机制 |
