# NL2SQL-Benchmark V1.0 技术设计（冻结版）

## 1. 目标

建立一套轻量、可扩展、可复现的 NL2SQL 统一评测脚手架。商业 API、开源系统和论文算法通过统一预测接口接入；数据库执行、指标计算和预测结果持久化由框架统一管理。

本版本只搭建脚手架，不实现具体算法、数据集解析、SQL 执行和指标计算。

## 2. 冻结范围

| 维度 | V1.0 决定 |
|---|---|
| 英文数据集 | Spider 2.0 |
| 中文数据集 | CSpider |
| Spider 2.0 | 首期只接入 SQLite 方言任务；其他方言任务显式跳过/标记 unsupported，不自动转换 |
| CSpider | 按数据集原生 SQLite 环境适配 |
| 首期执行数据库 | SQLite |
| 扩展数据库 | MySQL、PostgreSQL 预留 Executor 接口，不实现 |
| 算法输入 | Minimal：question、schema、dialect、context、sample_id |
| 算法输出 | sql、tables、columns、metadata、sample_id |
| 表字段提取 | 原生输出优先；缺失时允许由 SQL Parser 解析，并记录来源 |
| SQL 执行 | 由框架外部统一执行，不由算法适配器自行执行 |
| 结果保存 | 每次运行保存原始预测 JSONL 和运行配置快照 |
| 评估 | 可从历史预测重新计算，不重新调用模型 |

## 3. 分层架构

1. Dataset：加载样本、Schema、Gold 标签和数据库引用。
2. Core：定义统一输入输出对象及 `BaseNL2SQL`。
3. Methods：商业 API、开源项目、论文算法适配器。
4. Common：可选复用的 Schema、检索、Prompt、SQL 工具；不强制算法使用。
5. Storage：持久化原始预测和运行元数据。
6. Evaluation：统一 Executor 和指标评估。
7. Experiments：运行预测、重评估、横向比较。

## 4. 数据协议

### 4.1 InputData（算法可见）

- `sample_id`：数据集内稳定样本标识。
- `question`：当前自然语言问题。
- `schema`：统一结构化 Schema，至少包含 tables、columns、foreign_keys。
- `dialect`：目标 SQL 方言，例如 `sqlite`。
- `context`：可选业务上下文；多轮数据集可放置历史对话。

严禁向算法输入传递 Gold SQL、Gold Tables、Gold Columns 或用于评测的答案信息。

### 4.2 DatasetSample（框架内部）

由 `input_data`、`gold` 和 `database` 组成。Gold 标签与数据库引用只供 Runner / Evaluator 使用，不得透传到算法。

### 4.3 PredictionResult

- `sample_id`
- `sql`：允许为空，表示没有生成 SQL。
- `tables`：预测表标识列表；允许为空。
- `columns`：预测字段标识列表；允许为空。
- `metadata`：状态、模型、延迟、Token、错误信息、表字段来源等。

建议 `metadata` 至少预留：`status`、`latency`、`model`、`input_tokens`、`output_tokens`、`error`、`table_source`、`column_source`。

表字段来源应区分 `native`（算法原生输出）和 `sql_parser`（从生成 SQL 解析）。不得把解析结果伪装成算法原生 Schema Linking 输出。

## 5. 算法接口

所有方法继承 `BaseNL2SQL`，只要求实现 `predict(input_data) -> PredictionResult`。`close()` 用于释放资源。算法适配器不负责执行 SQL、不计算指标、不读取 Gold 标签。

对于运行在独立进程或服务中的开源项目，适配器通过 HTTP / SDK 调用即可；外部统一接口仍然是 `predict()`。

## 6. 数据集与方言策略

- Spider 2.0 包含多种数据库/工作流任务。首期只加载 SQLite 方言任务；其他方言任务必须明确记录为暂不支持，禁止静默改写成 SQLite。
- CSpider 按其 SQLite 数据库文件和原始标注格式适配。
- Dataset Loader 负责提供统一 Schema、Gold 标签和数据库引用。
- 数据集原始文件由使用者自行下载，不随脚手架打包。
- 后续新增数据集只需实现 `BaseDataset`，不应修改算法基类。

## 7. 数据库执行策略

统一 `BaseExecutor` 接口。首期实现目标为 `SQLiteExecutor`；本 scaffold 只提供接口占位。MySQL / PostgreSQL 仅预留适配文件。

预测 SQL 与 Gold SQL 必须在同一数据库快照、同一方言和一致的执行配置下运行。执行器需要预留只读保护、超时、错误捕获、结果规范化能力。

## 8. 评价指标规划

- SQL：官方规则 Exact Match、SQL Validity。
- 执行：Execution Success Rate、Execution Accuracy、Timeout Rate。
- 表：Table Precision / Recall / F1。
- 字段：Column Precision / Recall / F1。
- 性能：模型/算法预测延迟与 SQL 执行延迟分开统计；Mean、Median、P95。
- 成本：Token Usage；可获得可靠计价信息时统计 API Cost。

不同数据集优先遵循其官方评测规则。不能把 SQL 执行成功率当作执行准确率，也不能把 SQL 字符串相等简单等同于官方 Exact Match。

表/字段评价使用统一对象标识，并保留 native / sql_parser 来源。初期可统计完整 SQL 引用对象集合；后续可扩展到 SELECT、WHERE、JOIN、GROUP BY 等子句级指标。

## 9. 原始预测与实验可复现性

每个 run 独立保存：

- `predictions.jsonl`：逐样本原始预测。
- `run_config.yaml`：运行配置快照。
- `run_metadata.json`：run_id、时间、方法版本、Git Commit、数据集版本、随机种子、状态等。
- `metrics.json` / `report.md`：评估后生成。

原始预测文件按 run 追加写入，不覆盖历史 run。重新评估只读取预测、Gold 和数据库引用，不调用模型。

## 10. 明确不做的事情

V1.0 不建设 Web UI、不建设分布式调度、不训练模型、不自动下载数据集、不自动跨方言转换 SQL、不实现具体商业/开源/论文算法。
