# dist/ —— 交付给服务器项目的两个注入包

- `T/`：语义检索平铺条件 —— skills_flat/（16 个 skill）+ index.json（检索索引）+ retrieval_tool_spec.md（工具行为定义）
- `G/`：编排图指导条件 —— graph_tbox.yaml（编排图，语义定稿，字段名待按 KnowledgeGraphMiddleware 校准）+ metaplan_view.md（视图模板）

对接细节与决策见 `docs/对接与决策报告.md`（E1–E5 待拍板）。
