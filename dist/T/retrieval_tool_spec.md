# T 条件检索工具行为定义（skill_search）

**工具签名**：`skill_search(query: str, top_k: int = 3) -> list[{name, category, description, path}]`

**实现（从简，刻意不上向量检索）**：
1. 对 `index.json` 的 name + category + description 做大小写不敏感的关键词匹配（query 分词后计命中词数）；
2. 按命中数降序返回 top_k；零命中时返回全量 name+description 列表（让 agent 自己挑）；
3. agent 拿到 path 后用既有文件读取工具读 SKILL.md 全文。

**为什么从简**：本实验的对照变量是"编排结构"而非"检索质量"。向量检索引入嵌入模型、chunking、top-k 策略等新变量，会把 T→G 的差值污染成"检索器差异"。简化匹配对 16 个小库足够用——T 的真实瓶颈从来不在"找不到"，在"找到之后没有纪律约束怎么用"（这正是实验要验证的）。

**知识到达记录（分析用）**：每次 skill_search 调用与每次 SKILL.md 读取都落轨迹——分析时据此计算"检索次数/读取次数/检索后是否遵循"三个行为指标。
