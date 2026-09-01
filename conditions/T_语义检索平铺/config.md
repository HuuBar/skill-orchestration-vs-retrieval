# T 条件配置：语义检索平铺

- **skill 供给**：`skills/16个任务对口skill/` 平铺目录，agent 通过语义检索工具查询（query → top-k skill 文本），自由读取、组合。
- **不供给**：无预编图、无 metaplan 视图、无后验排序；图开关关闭（KnowledgeGraphMiddleware off，逐字节兼容）。
- **harness 其余部分完全相同**：账本/状态机/安全点/预算/E9 调度都在——T 不是"裸奔"，只是知识到达方式不同（这保证 T→G 差值可归因到编排结构而非 harness 有无）。
- **任务书**：与 G 完全相同的 goal 文本（recall≥0.70 前提下 neg_recall 0.457→0.65+），约束只出现在任务书里一次（模拟"注入"），不每轮重渲染。
