# skill 库占位（16 个任务对口 skill）

从 skillnet 检索结果导出后放入 `16个任务对口skill/`（每个 skill 一个目录，含 SKILL.md）。T/G 两条件用**同一批**，只有组织方式不同。

| 分组 | skill | 覆盖 |
|---|---|---|
| 数据管道 | pandas-pro (4.0k) | 68 设备 × 8 类 CSV 合并/时序 |
| 数据体检 | data-cleaning-pipeline-generator (14.3k)、ydata-profiling (34.3k) | 重复列/缺失/异常（对应事故 S2） |
| 特征工程 | ml-fundamentals (5.7k)、sota-data-cleaning-feature-selection-eda | 特征扩展 + 零重要度清理 |
| 模型训练 | xgboost (1.0k)、sklearn-model-trainer (8.5k)、training-pipelines (5.9k)、ml-model-training (6.9k)、early-stopping-callback (1.3k) | XGB/MLP、CV、超参、早停 |
| 评估 | model-evaluator (4.2k)、shap | 多指标 + CV 统计检验 + 可解释性 |
| 分类专项 | ce-classification (3.0k) | 分类语义 |
| 实验方法 | statistical-analysis (19.4k)、MLflow Patterns (10.5k)、autoresearch (11.1k) | 消融/显著性、实验追踪、改-测-留/弃 |

> 注意：若某 skill 找不到原始文件，用同名占位 + 一行说明即可——本实验比较的是组织方式，skill 文本细节两边一致即可，但**严禁两边内容不一致**。
