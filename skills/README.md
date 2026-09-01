# skill 库（16 个任务对口 skill，已就位）

**来源**：`github.com/majiayu000/claude-skill-registry`（skillnet 同源注册表），2026-09-01 下载。16/16 全部找到原文，其中 15 个与 skillnet 检索记录的字节数精确吻合；两个特例：
- `statistical-analysis`：按 19.4k 记录取自 `skills/data/` 类目版（`skills/analysis/` 下有同名 5.8k 版本，非本实验所用）；
- `autoresearch`：取 `autoresearch-ml` 变体（13.5k），内容吻合检索记录描述的"改-测-留/弃"迭代循环（edit → train → measure → keep/revert）。

T/G 两条件用**同一批**，只有组织方式不同——严禁两边内容不一致。

| 分组 | skill | 覆盖 |
|---|---|---|
| 数据管道 | pandas-pro (4.0k) | 68 设备 × 8 类 CSV 合并/时序 |
| 数据体检 | data-cleaning-pipeline-generator (14.3k)、ydata-profiling (34.3k) | 重复列/缺失/异常（对应事故 S2） |
| 特征工程 | ml-fundamentals (5.7k)、sota-data-cleaning-feature-selection-eda | 特征扩展 + 零重要度清理 |
| 模型训练 | xgboost (1.0k)、sklearn-model-trainer (8.5k)、training-pipelines (5.9k)、ml-model-training (6.9k)、early-stopping-callback (1.3k) | XGB/MLP、CV、超参、早停 |
| 评估 | model-evaluator (4.2k)、shap | 多指标 + CV 统计检验 + 可解释性 |
| 分类专项 | ce-classification (3.0k) | 分类语义 |
| 实验方法 | statistical-analysis (19.4k)、mlflow-patterns (10.5k)、autoresearch (13.5k) | 消融/显著性、实验追踪、改-测-留/弃 |
