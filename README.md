# NL2SQL-Benchmark

统一的 NL2SQL 算法评测脚手架（V1.0 scaffold）。

> 当前版本只搭建项目结构、数据协议和接口占位，不包含可运行的完整数据集解析、模型调用、SQL 执行或指标计算实现。尚未实现的功能均以 `TODO` 标记。

## 1. V1.0 范围

| 项目 | 当前范围 |
|---|---|
| 英文数据集 | Spider 2.0（首期仅处理 SQLite 方言任务） |
| 中文数据集 | CSpider |
| 数据库执行 | SQLite 适配器接口；实际连接与执行待实现 |
| 其他数据库 | MySQL / PostgreSQL 仅保留扩展接口 |
| 算法类型 | 商业 API、开源项目、论文算法适配目录 |
| 统一输入 | `InputData`：问题、Schema、方言、可选上下文 |
| 统一输出 | `PredictionResult`：SQL、Tables、Columns、Metadata |
| 评估 | 独立模块占位，暂不实现指标逻辑 |
| 结果保存 | JSONL Store 接口占位，暂不实现读写逻辑 |

## 2. 目录结构

```text
nl2sql-benchmark/
├── config/                  # 数据集、方法、实验配置模板
├── docs/                    # 架构与评测约定
├── src/nl2sql_benchmark/
│   ├── core/                 # 输入、输出和算法基类
│   ├── datasets/             # Spider 2.0、CSpider 数据集适配器
│   ├── methods/              # 商业、开源、论文算法适配目录
│   ├── common/               # 可复用工具模块占位
│   ├── evaluation/           # Executor 与 Evaluator 接口
│   ├── storage/              # 原始预测结果存储接口
│   └── experiments/          # 运行、重评估、对比入口占位
├── tests/                    # 测试计划占位
├── results/                  # 实验输出目录（不提交真实结果）
├── DESIGN.md                 # 冻结的 V1.0 技术设计
└── TODO.md                   # 后续开发任务清单
```

## 3. 环境要求

- Python 3.10+
- SQLite：首期目标数据库；Python 标准库提供 `sqlite3`
- 依赖清单见 `pyproject.toml` 和 `requirements.txt`

## 4. 当前状态

本仓库是 scaffold，不应期待以下命令已经可以完成真实实验：

- 下载或解析 Spider 2.0 / CSpider 数据集
- 调用商业 API、开源服务或论文模型
- 执行 SQL 或计算准确率
- 生成真实实验报告

这些功能已在对应模块留下接口和 TODO。完成实现后，再补充正式 CLI 用法和端到端运行示例。

## 5. 设计入口

- [冻结设计](DESIGN.md)
- [开发任务清单](TODO.md)
- [架构说明](docs/architecture.md)
- [数据集与数据库约定](docs/datasets-and-dialects.md)
- [本地开发数据说明](docs/dev-data.md)
- [指标口径](docs/metrics.md)

## 6. 安全与数据管理

- 不要将 API Key、数据库密码或私有数据提交到 Git。
- 数据集原始文件默认由使用者自行下载并放在本地数据目录。
- Gold SQL、Gold Tables、Gold Columns 只能进入 Dataset / Evaluation 路径，不得放入算法的 `InputData`。
- 原始预测结果建议按 run 独立保存；已生成的 run 不应被后续实验覆盖。
