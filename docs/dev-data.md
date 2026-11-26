# 本地开发数据说明（Spider 2.0 / CSpider）

本文记录为后续 Loader 与评测开发准备的一小批真实数据：官方来源、本地目录、
开发样本清单、Gold 资源情况和下载步骤。数据只保存在本地（`data/` 已被
`.gitignore` 排除），不提交到 Git。

当前 Loader 尚未实现，`config/datasets.yaml` 中的路径仅为约定，尚未生效。

## 1. Spider 2.0-Lite（SQLite 任务）

### 来源与版本

| 资源 | 官方来源 | 本次实际使用的渠道 |
|---|---|---|
| 任务文件、Gold SQL、Gold 执行结果、评测脚本 | https://github.com/xlang-ai/Spider2 （`spider2-lite/`） | GitHub raw，取自 `main` 分支，提交 `cafb867313aa`（2026-08-12） |
| SQLite 数据库（spider2-localdb） | 官方 Google Drive 链接（见 `spider2-lite/README.md`） | Google Drive 在当前网络不可达；改用官方组织 XLang Lab 在 ModelScope 的镜像 `xlangai/spider2-localdb`（`sqlite.zip`，上传于 2025-08-18） |

注意：ModelScope/HF 镜像上的 `sqlite.zip` 是**较早一代**的 localdb 打包
（部分数据库文件名与当前任务文件的 `db` 名不一致，例如 `sakila_master.sqlite`
对应现在的 `sqlite-sakila`）。因此本次只选用**文件名与任务 `db` 名完全一致**
的数据库（`IPL.sqlite`、`Pagila.sqlite`），并通过官方 Gold SQL 实跑比对官方
Gold 执行结果做了验证（见下文）。后续网络可达时，建议按官方 README 从
Google Drive 重新下载当前代 localdb 覆盖。

### 本地目录

```text
data/spider2/
├── dev_manifest.json                 # 开发样本清单（6 个任务）
├── _downloads/sqlite.zip             # 官方镜像整包存档（573MB，仅本地保留）
└── spider2-lite/                     # 沿用官方 spider2-lite 目录布局
    ├── spider2-lite.jsonl            # 官方任务文件（547 条，其中 135 条 local/SQLite 任务）
    ├── README.md
    ├── evaluation_suite/
    │   ├── evaluate.py               # 官方评测脚本（exec_result 模式可直接复用）
    │   ├── evaluate_utils.py
    │   └── gold/
    │       ├── spider2lite_eval.jsonl  # 官方逐样本评测配置（condition_cols/ignore_order）
    │       ├── sql/local022.sql ...    # 4 个选定样本的官方 Gold SQL
    │       └── exec_result/localXXX_*.csv  # 9 个 Gold 执行结果 CSV
    └── resource/databases/spider2-localdb/
        ├── IPL.sqlite               # 12.6MB
        └── Pagila.sqlite            # 5.8MB
```

### 开发样本清单（6 个 SQLite 任务，2 个数据库）

清单文件：`data/spider2/dev_manifest.json`。样本的 `instance_id` 为 Spider 2.0-Lite
原始任务标识，`db` 与 SQLite 文件按官方 `evaluate.py` 的规则一一对应
（`{db}.sqlite`）。

| instance_id | db | Gold SQL | Gold 执行结果 |
|---|---|---|---|
| local038 | Pagila | 有 | 2 个结果变体 |
| local039 | Pagila | 有 | 2 个结果变体 |
| local022 | IPL | 有 | 1 个结果变体 |
| local023 | IPL | 有 | 1 个结果变体 |
| local020 | IPL | 无（官方未公开） | 2 个结果变体 |
| local021 | IPL | 无（官方未公开） | 1 个结果变体 |

说明：官方对全部 135 个 SQLite 任务都提供了 Gold 执行结果 CSV，但只对 24 个
任务公开了 Gold SQL；本清单特意保留了无 Gold SQL 的样本，以覆盖两种评价输入。
所有选定样本都不需要外部知识文档（`external_knowledge` 为空）。

## 2. CSpider（中文 dev）

### 来源与版本

| 资源 | 官方来源 | 本次实际使用的渠道 |
|---|---|---|
| dev.json（1034 条中文问题 + SQL） | 官方任务站 https://taolusi.github.io/CSpider-explorer/ （Google Drive / 百度网盘） | 官方渠道在当前网络不可达或无法脚本化下载；改用 GitHub 镜像 `pengtao819/CSpider-Text-to-SQL-Finetuning` 的 `data/raw/dev.json`（提交 `f959dfc0c2c9`），已验证为官方 Spider 格式、1034 条、20 个库、中文问题 |
| tables.json、database/（SQLite） | CSpider 复用 Spider 1.0 官方数据包 | ModelScope 镜像 `ModelM/spider` 的 `spider.zip`（官方 Spider 数据包，README 标注 2020-08-03 更新版） |
| dev_gold.sql | CSpider 官方包内含 `dev_glod.sql` | 未单独使用；Gold SQL 直接取自 dev.json 的 `query` 字段（同一文件内部一致） |

已验证的一致性：CSpider `dev.json` 共 1034 条，与 Spider 官方 2020 版
`dev_gold.sql` 逐行比对 690 行完全一致，其余 344 行为大小写或 2020 年官方
标注修正差异——说明 CSpider dev 冻结的是较早的 Spider dev 版本，因此**不要**
把 2020 版 `dev_gold.sql` 混用作 CSpider 的 Gold，统一以 `dev.json` 的
`query` 字段为准。

### 本地目录

```text
data/cspider/
├── dev_manifest.json               # 开发样本清单（18 个样本）
├── _downloads/spider.zip           # 官方 Spider 数据包存档（99.7MB，仅本地保留）
└── cspider/
    ├── dev.json                    # CSpider 官方 dev（1034 条，含中文问题与 Gold SQL）
    ├── tables.json                 # Spider 官方 schema（原英文表名列名）
    └── database/
        ├── concert_singer/  concert_singer.sqlite(36KB) + schema.sql
        ├── pets_1/          pets_1.sqlite(16KB) + schema.sql
        └── car_1/           car_1.sqlite(64KB) + car_1.sql
```

### 开发样本清单（18 个样本，3 个数据库）

清单文件：`data/cspider/dev_manifest.json`。`dev_index` 保留样本在官方
`dev.json` 中的原始行索引（0 起），问题与 Gold SQL 为原文未改写。

| db_id | 样本数 | dev.json 索引 |
|---|---|---|
| concert_singer | 6 | 0, 5, 10, 20, 25, 30 |
| pets_1 | 6 | 45, 49, 53, 61, 65, 73 |
| car_1 | 6 | 87, 97, 107, 117, 137, 157 |

## 3. 已知限制

1. **Spider 2.0-Lite 当前代 localdb 未下载成功**：官方 Google Drive 在当前
   网络不可达，官方组织在 ModelScope/HF 的镜像整包（573MB）是较早一代命名。
   已选数据库通过 Gold SQL 实跑与官方 Gold 结果比对验证一致；如需其余 28 个
   库，需从 Google Drive 重新获取。
2. **CSpider 官方中文 tables.json 未获取**：官方包（百度网盘
   `pan.baidu.com/s/1B84p7Wl8jx9F3nd0xpt4hw`，无提取码）在当前环境无法脚本化
   下载。暂用 Spider 官方 `tables.json`（原英文表名列名，与 SQLite 文件和
   Gold SQL 使用的标识一致）。后续拿到官方包后可直接替换并保留中文映射。
3. 两个 `_downloads/` 存档仅本地保留，用于追溯来源；不需要时可删除。

## 4. 下载与筛选步骤（实际使用的命令）

Spider 2.0-Lite：

```bash
# 任务文件与评测套件（GitHub raw）
curl -sL -o data/spider2/spider2-lite/spider2-lite.jsonl \
  https://raw.githubusercontent.com/xlang-ai/Spider2/main/spider2-lite/spider2-lite.jsonl
# evaluation_suite/{README.md,evaluate.py,evaluate_utils.py,gold/spider2lite_eval.jsonl} 同理

# Gold SQL：先从 GitHub contents API 列出 evaluation_suite/gold/sql 下
# 以 local 开头的文件（共 24 个），再按清单下载对应 localXXX.sql

# SQLite 数据库（官方 Google Drive 不可达，改用 ModelScope 官方组织镜像）
curl -sL -o data/spider2/_downloads/sqlite.zip \
  https://modelscope.cn/datasets/xlangai/spider2-localdb/resolve/master/sqlite.zip
# 解压后仅保留文件名与任务 db 名一致的 IPL.sqlite、Pagila.sqlite
```

CSpider：

```bash
# dev.json（GitHub 镜像，校验大小 3,814,873 字节）
curl -sL -o data/cspider/cspider/dev.json \
  https://raw.githubusercontent.com/pengtao819/CSpider-Text-to-SQL-Finetuning/main/data/raw/dev.json

# tables.json 与数据库（ModelScope 官方 Spider 数据包镜像）
curl -sL -o data/cspider/cspider/tables.json \
  https://modelscope.cn/datasets/ModelM/spider/resolve/master/tables.json
curl -sL -o data/cspider/_downloads/spider.zip \
  https://modelscope.cn/datasets/ModelM/spider/resolve/master/spider.zip
# 解压仅保留 concert_singer / pets_1 / car_1 三个库的 sqlite 与 schema
```

## 5. 最小验证方法

验证使用一次性脚本完成（不随仓库提交），核心步骤可手动重放：

1. 清单中的每个样本能找到对应数据库文件；
2. `sqlite3` 以只读模式打开数据库并列出表；
3. 有 Gold SQL 的样本在本地库上执行 Gold SQL，与官方 Gold 执行结果
   （规范化为行集合后）比对；
4. CSpider 样本的本地库表集合与 `tables.json` 中该库的 `table_names_original`
   一致，且 dev.json 的 Gold SQL 可执行。

验证结果（2026-11-26）：

- Spider 2.0-Lite：6 个样本数据库均可打开读取表结构；4 个 Gold SQL 实跑，
  local022/local038/local039 的执行结果与官方 Gold 结果 CSV **精确一致**。
  local023 的公开 Gold SQL 与 Gold 结果 CSV 是官方工件本身的口径差异
  （SQL 输出 1 列四舍五入均值，CSV 为 2 列），公共列四舍五入后一致，
  不影响该样本作为开发数据使用（评价以 Gold 结果 CSV 为准）。
  另外用其余同名库抽查了 4 个 Gold 任务（local008/219/210/309）：local008
  精确一致（仅下划线/空格格式差异）；local219/210/309 行数一致但个别行的
  口径或构造器归属不同——同样是官方 Gold SQL 变体与 Gold 结果变体之间的
  差异，未见数据库内容代差。
- CSpider：18 个样本全部通过（表结构与 `tables.json` 一致、Gold SQL 可执行）。

## 6. 后续下载完整数据的补充资源

- Spider 2.0-Lite 全量 SQLite：官方 Google Drive localdb 包
  （`spider2-lite/README.md` 中的链接），解压放入
  `spider2-lite/resource/databases/spider2-localdb/`。
- Spider 2.0-Lite 全部外部知识文档：仓库 `spider2-lite/resource/documents/`。
- CSpider 官方完整包（含中文 tables.json、train 数据、dev_glod.sql、全部
  数据库）：任务站提供的 Google Drive 或百度网盘链接。
