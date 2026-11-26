# V1.0 开发任务清单

> 本文件记录待开发项。当前 scaffold 不代表这些功能已实现。

## P0：框架基础

- [ ] 完成 `InputData`、`GoldData`、`DatabaseRef`、`DatasetSample` 的校验与序列化。
- [ ] 完成 `PredictionResult` 规范化、状态枚举和序列化。
- [ ] 完成 `BaseNL2SQL` 调用封装、异常处理和资源释放。
- [ ] 明确样本 ID、表标识、字段标识的规范。

## P0：数据集

- [ ] 实现 Spider 2.0 数据下载说明与本地目录检查。
- [ ] 实现 Spider 2.0 SQLite 方言任务筛选与 Loader。
- [ ] 对 Spider 2.0 非 SQLite 任务记录 unsupported/skipped 原因。
- [ ] 实现 CSpider Loader 与 Schema 映射。
- [ ] 实现 Gold SQL / Gold Tables / Gold Columns 的独立读取。
- [ ] 验证数据库文件、样本、Gold 标注之间的关联完整性。

## P0：数据库执行

- [ ] 实现 SQLite 连接与执行。
- [ ] 增加只读执行保护。
- [ ] 增加执行超时、异常捕获和资源清理。
- [ ] 定义结果集规范化规则（排序、重复行、NULL、浮点数等）。
- [ ] 编写 SQLite Executor 单元测试。

## P0：算法适配

- [ ] 增加至少一个 Mock 方法用于接口集成测试（仅测试用途）。
- [ ] 定义商业 API 适配器模板。
- [ ] 定义开源服务适配器模板。
- [ ] 定义论文算法适配器模板。
- [ ] 统一记录模型、Prompt、Token、调用耗时和错误信息。

## P0：预测存储与实验运行

- [ ] 实现 JSONL 原始预测写入与读取。
- [ ] 实现 run_id 和独立 run 目录。
- [ ] 保存配置、Git Commit、数据集版本和方法版本。
- [ ] 实现失败样本记录与断点续跑。
- [ ] 保证重评估不触发算法调用。

## P0：评价

- [ ] 接入 Spider 2.0 对应的官方评测逻辑（SQLite 任务范围）。
- [ ] 接入 CSpider 对应的 SQL 评价规则。
- [ ] 实现 SQL Validity、Execution Success、Execution Accuracy。
- [ ] 实现 Table / Column Precision、Recall、F1。
- [ ] 实现算法预测耗时与 SQL 执行耗时的分离统计。
- [ ] 实现 Mean、Median、P95、Timeout Rate。
- [ ] 实现 Token Usage；API Cost 仅在有可靠计价信息时统计。
- [ ] 实现样本级、宏平均和微平均结果。

## P1：扩展能力

- [ ] 实现 MySQL Executor。
- [ ] 实现 PostgreSQL Executor。
- [ ] 扩展 Spider 2.0 BigQuery / Snowflake / DuckDB 等方言与执行环境。
- [ ] 支持更多中文数据集和多轮对话数据集。
- [ ] 支持子句级 Table / Column 指标。

## 验收清单

- [ ] Spider 2.0 SQLite 子集可以通过统一 Loader 加载。
- [ ] CSpider 可以通过统一 Loader 加载。
- [ ] 算法输入不包含任何 Gold 信息。
- [ ] 商业 API、开源服务、论文算法遵循同一 `predict()` 协议。
- [ ] SQL 执行由框架 Executor 统一完成。
- [ ] 预测结果按 run 保存，且历史 run 不被覆盖。
- [ ] 可以只用历史预测重新计算指标，不调用模型。
- [ ] 指标通过人工构造的边界样例测试。
- [ ] 报告明确区分 SQL Validity、Execution Success 和 Execution Accuracy。
- [ ] README、配置说明和扩展开发说明完整。
