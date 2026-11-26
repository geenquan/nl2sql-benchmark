# 本地开发数据说明（Spider 2.0 / CSpider）

本文记录为后续 Loader 与评测开发准备的一小批真实数据：官方来源、本地目录、
开发样本清单、Gold 资源情况和已做的验证。数据只保存在本地（`data/` 已被
`.gitignore` 排除），不提交到 Git。

当前 Loader 尚未实现，`config/datasets.yaml` 中的路径仅为约定，尚未生效。

## 1. Spider 2.0-Lite（SQLite 任务）

### 来源与版本

| 资源 | 官方渠道 | 本次实际使用的渠道与版本 |
|---|---|---|
| 任务文件、Gold SQL、Gold 执行结果、评测脚本 | https://github.com/xlang-ai/Spider2 （`spider2-lite/`） | GitHub raw，按固定提交 `cafb867313aa` 获取（2026-08-12 提交） |
| SQLite 数据库（spider2-localdb） | 官方 Google Drive 链接（见 `spider2-lite/README.md`） | Google Drive 在当前网络不可达；改用官方组织 XLang Lab 在 ModelScope 的镜像 `xlangai/spider2-localdb`（`sqlite.zip`，2025-08-18 上传） |

注意：该镜像的 `sqlite.zip` 是**较早一代**的 localdb 打包（部分数据库文件名
与当前任务文件的 `db` 名不一致，例如 `sakila_master.sqlite` 对应现在的
`sqlite-sakila`）。本次只选用**文件名与任务 `db` 名完全一致**的两个库
（`IPL.sqlite`、`Pagila.sqlite`），并对 Gold SQL 非空的样本做了实跑比对
（见下文验证说明）。这两个库来自较早的打包快照，**尚未证明**与当前官方
Google Drive 版本的数据库内容完全一致，目前仅用于开发用途。后续网络可达时，
建议按官方 README 从 Google Drive 重新下载当前代 localdb 覆盖。

### 本地目录

```text
data/spider2/
├── dev_manifest.json                 # 开发样本清单（5 个任务）
├── _downloads/sqlite.zip             # 官方镜像整包存档（573MB，仅本地保留）
└── spider2-lite/                     # 沿用官方 spider2-lite 目录布局
    ├── spider2-lite.jsonl            # 官方任务文件（547 条，其中 135 条 local/SQLite 任务）
    ├── README.md
    ├── evaluation_suite/
    │   ├── evaluate.py               # 官方评测脚本（本地未运行过）
    │   ├── evaluate_utils.py
    │   └── gold/
    │       ├── spider2lite_eval.jsonl  # 官方逐样本评测配置（condition_cols/ignore_order）
    │       ├── sql/localXXX.sql        # 4 个 Gold SQL（含已排除的 local023.sql，原始资源保留）
    │       └── exec_result/localXXX_*.csv  # 9 个 Gold 执行结果 CSV（含已排除的 local023_a.csv）
    └── resource/databases/spider2-localdb/
        ├── IPL.sqlite               # 12.6MB
        └── Pagila.sqlite            # 5.8MB
```

### 开发样本清单（5 个 SQLite 任务，2 个数据库）

清单文件：`data/spider2/dev_manifest.json`。样本的 `instance_id` 为 Spider 2.0-Lite
原始任务标识，`db` 与 SQLite 文件按官方 `evaluate.py` 的规则一一对应
（`{db}.sqlite`）。

| instance_id | db | Gold SQL | Gold 执行结果 | 一致性验证状态 |
|---|---|---|---|---|
| local038 | Pagila | 有 | 2 个结果变体 | 结果完全一致（与变体 local038_a.csv 精确比对通过） |
| local039 | Pagila | 有 | 2 个结果变体 | 结果完全一致（与变体 local039_b.csv 精确比对通过） |
| local022 | IPL | 有 | 1 个结果变体 | 结果完全一致（与变体 local022_a.csv 精确比对通过） |
| local020 | IPL | 无（官方未公开） | 2 个结果变体 | 尚未验证（保留用于加载与结果路径开发） |
| local021 | IPL | 无（官方未公开） | 1 个结果变体 | 尚未验证（保留用于加载与结果路径开发） |

"结果完全一致"指：在本地库上执行官方 Gold SQL，把结果行集合与官方 Gold
执行结果 CSV（去掉表头）做**排序后的逐单元格字符串精确比对**，与某个结果
变体完全一致。这是我们做的简化代理检查，**不是**官方 `evaluate.py` 的完整
比较逻辑（官方脚本本地没有运行过）；`ignore_order=true` 的语义按官方配置
记录在清单中，尚未用官方比较流程复核。

排除说明：`local023`（IPL）未纳入清单——官方公开的 Gold SQL 输出 2 列
（`player_name`, `batting_avg`），而 Gold 结果 CSV 为 3 列（`player_name`,
`avg_runs_per_match`, `batting_average`），列数不一致；其评测配置
`condition_cols=[]` 也未声明只比较公共列。原始 SQL、CSV 与数据库文件保留在
本地，未做任何修改。

说明：官方对全部 135 个 SQLite 任务都提供了 Gold 执行结果 CSV，但只对 24 个
任务公开了 Gold SQL；清单保留 2 个无 Gold SQL 的样本，用于加载与 Gold 结果
路径开发，不能声称其已通过与数据库的一致性验证。所有选定样本都不需要外部
知识文档（`external_knowledge` 为空）。

## 2. CSpider（中文 dev）

### 来源与版本

| 资源 | 官方渠道 | 本次实际使用的渠道与版本 |
|---|---|---|
| dev.json（1034 条中文问题 + SQL） | 官方任务站 https://taolusi.github.io/CSpider-explorer/ （Google Drive / 百度网盘） | 官方渠道在当前网络不可达或无法脚本化下载；改用第三方 GitHub 镜像 `pengtao819/CSpider-Text-to-SQL-Finetuning` 的 `data/raw/dev.json`，按固定提交 `f959dfc0c2c9` 获取 |
| tables.json、database/（SQLite） | CSpider 复用 Spider 1.0 官方数据包 | ModelScope 镜像 `ModelM/spider` 的 `spider.zip` 与 `tables.json`（包内 README 标注为官方 2020-08-03 更新版；ModelScope 无固定版本 URL，下载于 2026-11-26） |
| dev_gold.sql | CSpider 官方包内含 `dev_glod.sql` | 未单独使用；Gold SQL 直接取自 dev.json 的 `query` 字段（同一文件内部一致） |

来源说明：**CSpider 标注（dev.json）与 Schema/数据库（tables.json、SQLite）
目前来自不同渠道**——前者是第三方 GitHub 镜像，后者是 ModelScope 上的官方
Spider 数据包镜像。dev.json 已核对的仅限格式层面（1034 条、20 个库、中文
问题、字段结构与 Spider dev 格式一致），**尚未与官方原始发布包逐字段核对**。

已做的交叉比对（观察事实）：dev.json 的 1034 条 `query`+`db_id` 与 ModelM
镜像内 Spider 官方 2020 版 `dev_gold.sql` 逐行比对，690 行完全一致，344 行
存在差异；差异中可见大小写不同和个别 SQL 语义不同的样本，具体原因（官方
后续修订、解析器重写或其他）**未逐一核实**。因此未将 2020 版 `dev_gold.sql`
用作 CSpider 的 Gold，统一以 `dev.json` 的 `query` 字段为准。

### 本地目录

```text
data/cspider/
├── dev_manifest.json               # 开发样本清单（12 个样本，含排除记录）
├── _downloads/spider.zip           # 官方 Spider 数据包存档（99.7MB，仅本地保留）
└── cspider/
    ├── dev.json                    # dev 标注（1034 条，中文问题与 SQL）
    ├── tables.json                 # Spider 官方 schema（原英文表名列名）
    └── database/
        ├── concert_singer/  concert_singer.sqlite(36KB) + schema.sql
        ├── pets_1/          pets_1.sqlite(16KB) + schema.sql
        └── car_1/           car_1.sqlite(64KB) + car_1.sql
```

### 开发样本清单（12 个样本，3 个数据库）

清单文件：`data/cspider/dev_manifest.json`。`dev_index` 保留样本在 `dev.json`
中的原始行索引（0 起），问题与 Gold SQL 为原文未改写。

| db_id | 样本数 | dev.json 索引 |
|---|---|---|
| concert_singer | 5 | 0, 10, 20, 25, 30 |
| pets_1 | 3 | 45, 49, 73 |
| car_1 | 4 | 87, 97, 107, 117 |

排除记录（6 条，详见清单 `excluded` 字段）：dev_index 5、53、61、65、137、
157。共同原因是 Gold SQL 中的**中文字符串条件值在数据库中不存在**——数据库
实际存储英文值（`country='France'`、`sex='F'`、`pettype='cat'/'dog'`、
`Model` 为 33 个英文品牌名，无 geely）。这是 CSpider 翻译数据与我们这批
英文库值之间的现象，原始 dev.json、数据库均未修改，也未手工翻译条件值。
保留样本的 Gold SQL 不含任何字符串字面量条件，不存在这类不匹配。

Schema 说明：未获取 CSpider 官方发布包中的中文映射文件，暂用 Spider 官方
`tables.json`（原英文表名列名）。英文表字段名与 SQLite 库和 Gold SQL 使用的
标识一致，本身不代表资源错误；是否需要补齐官方中文映射，待 Loader 开发时
按实际需求确认，当前不做定论。

## 3. 已知限制

1. **Spider 2.0-Lite 数据库来自较早镜像**：官方 Google Drive 在当前网络
   不可达，官方组织在 ModelScope/HF 的镜像整包（573MB）是较早一代命名与
   打包。已选 2 个库对 Gold SQL 非空样本做了实跑比对（3/3 精确一致），
   但**不能证明**与当前官方数据库快照完全一致。
2. **CSpider 标注与 Schema/数据库来自不同渠道**：dev.json 为第三方镜像
   （仅格式层面核对），tables.json 与数据库为 ModelScope 官方 Spider 包
   镜像。中文问题中的条件值与英文库值不匹配的样本已从清单排除；其余样本
   的语义正确性未进一步验证。
3. 两个 `_downloads/` 存档仅本地保留，用于追溯来源；不需要时可删除。

## 4. 下载与筛选步骤（实际使用的命令）

Spider 2.0-Lite：

```bash
# 任务文件与评测套件（GitHub raw，固定提交 cafb867313aa，可按同版本重取）
curl -sL -o data/spider2/spider2-lite/spider2-lite.jsonl \
  https://raw.githubusercontent.com/xlang-ai/Spider2/cafb867313aa/spider2-lite/spider2-lite.jsonl
# evaluation_suite/{README.md,evaluate.py,evaluate_utils.py,gold/spider2lite_eval.jsonl}
# 与 gold/sql/localXXX.sql、gold/exec_result/localXXX_*.csv 同理，URL 中
# main 替换为 cafb867313aa 即可按固定版本重取

# Gold SQL 候选名单：通过 GitHub contents API 列出
# evaluation_suite/gold/sql 下以 local 开头的文件（当时共 24 个）

# SQLite 数据库（官方 Google Drive 不可达，改用 ModelScope 官方组织镜像；
# 该资源无固定版本 URL，记录下载日期 2026-11-26，未提供校验值）
curl -sL -o data/spider2/_downloads/sqlite.zip \
  https://modelscope.cn/datasets/xlangai/spider2-localdb/resolve/master/sqlite.zip
# 解压后仅保留文件名与任务 db 名一致的 IPL.sqlite、Pagila.sqlite
```

CSpider：

```bash
# dev.json（第三方 GitHub 镜像，固定提交 f959dfc0c2c9，校验大小 3,814,873 字节）
curl -sL -o data/cspider/cspider/dev.json \
  https://raw.githubusercontent.com/pengtao819/CSpider-Text-to-SQL-Finetuning/f959dfc0c2c9/data/raw/dev.json

# tables.json 与数据库（ModelScope 官方 Spider 数据包镜像；revision=master，
# 无固定版本 URL 与校验值，下载日期 2026-11-26）
curl -sL -o data/cspider/cspider/tables.json \
  https://modelscope.cn/datasets/ModelM/spider/resolve/master/tables.json
curl -sL -o data/cspider/_downloads/spider.zip \
  https://modelscope.cn/datasets/ModelM/spider/resolve/master/spider.zip
# 解压仅保留 concert_singer / pets_1 / car_1 三个库的 sqlite 与 schema
```

## 5. 最小验证方法与结果

验证使用终端内一次性只读脚本完成（未新增脚本文件、未运行官方评测脚本），
核心步骤可手动重放：

1. 清单可解析，`selected_count` 与实际条数一致；
2. 每个样本能对应到原始标注（CSpider 按 `dev_index` 回读 dev.json 比对
   question 与 gold_sql）和本地数据库文件；
3. SQLite 以只读模式打开并列出表；CSpider 各库表集合与 `tables.json` 中该库
   的 `table_names_original` 一致；
4. CSpider：提取每条 Gold SQL 中的字符串字面量，逐一与目标库全部列值做
   大小写不敏感比对，未命中的样本从清单排除；
5. Spider 2.0-Lite：Gold SQL 非空的样本在本地库执行官方 Gold SQL，结果行
   集合与官方 Gold 结果 CSV 做排序后逐单元格字符串精确比对。

验证结果（2026-11-26，本次修正后）：

- Spider 2.0-Lite：5 个样本数据库均可打开读取表结构；3 个 Gold SQL 非空样本
  实跑，结果与官方 Gold 结果变体**完全一致**（local022→a、local038→a、
  local039→b，精确字符串比对）；2 个无 Gold SQL 样本尚未验证。比对为简化
  代理检查，官方 `evaluate.py` 比较逻辑本地未运行。
  另曾用同一方法抽查镜像中其他 4 个同名库的 Gold 任务（local008/219/210/309）：
  local008 结果在忽略大小写和下划线/空格差异后一致；local219/210/309 行数
  一致但个别行取值不同（如 f1 任务 75 行中 8 行的构造器归属不同）。这些
  差异发生在官方 Gold SQL 与 Gold 结果变体之间，具体原因未核实；因此不能
  据此断定镜像库与当前官方库一致或不一致，上述 4 个库也未纳入开发清单。
- CSpider：12 个保留样本全部通过上述检查（库表一致、Gold SQL 可执行、
  无字符串字面量未命中）；6 个含中文条件值不匹配的样本已排除并记录原因。

仍未核实的内容：CSpider dev.json 与官方原始包的逐字段一致性；Spider 2.0
本地库与官方当前 Google Drive 快照的一致性；官方比较逻辑下的评测结果；
各 Gold SQL 与 Gold 结果变体之间的口径差异（如 local023 的列数差异、
EU_soccer/f1 抽查中个别行的构造器归属差异）的官方解释。

## 6. 后续下载完整数据的补充资源

- Spider 2.0-Lite 全量 SQLite：官方 Google Drive localdb 包
  （`spider2-lite/README.md` 中的链接），解压放入
  `spider2-lite/resource/databases/spider2-localdb/`。
- Spider 2.0-Lite 全部外部知识文档：仓库 `spider2-lite/resource/documents/`。
- CSpider 官方完整包（含中文映射 tables.json、train 数据、dev_glod.sql、全部
  数据库）：任务站提供的 Google Drive 或百度网盘链接。
