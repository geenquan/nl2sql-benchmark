# 数据集与数据库方言约定

## V1.0 数据集

| Dataset | Language | 首期方言范围 | 说明 |
|---|---|---|---|
| Spider 2.0 | English | SQLite tasks only | 其他方言任务标记 unsupported，不自动转换 |
| CSpider | Chinese | SQLite | 按原始数据集格式适配 |

## 数据目录约定（建议）

```text
data/
├── spider2/
│   └── ...  # 用户自行放置官方数据及数据库文件
└── cspider/
    └── ...  # 用户自行放置数据集及 SQLite 文件
```

实际文件布局以下载版本为准，Loader 实现时再确认，不在 scaffold 阶段假设固定文件名。

## 方言扩展

- 当前目标：SQLite。
- 预留：MySQL、PostgreSQL。
- Spider 2.0 其他任务涉及的 BigQuery、Snowflake、DuckDB 等环境不在本次实现范围。
- 不允许为了统一执行而静默把一种方言 SQL 改写为 SQLite。

## Schema 统一表示

Schema 至少包含：

- `tables`
- `columns`
- `foreign_keys`

具体字段结构由 Loader 实现时统一，并记录原始名称与规范化名称的映射。
