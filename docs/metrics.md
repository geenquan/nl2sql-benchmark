# 指标口径（实现待办）

| 指标 | 含义 | 注意事项 |
|---|---|---|
| Exact Match | SQL 与 Gold SQL 的结构/官方匹配 | 使用数据集官方规则，不用简单字符串相等替代 |
| SQL Validity | SQL 是否符合目标方言语法 | 与执行成功分开统计 |
| Execution Success Rate | SQL 是否成功执行 | 只代表执行成功，不代表答案正确 |
| Execution Accuracy | 预测 SQL 结果是否与 Gold SQL 结果一致 | 遵循数据集官方结果比较规则 |
| Table P/R/F1 | 表集合识别质量 | 统一表标识，记录预测来源 |
| Column P/R/F1 | 字段集合识别质量 | 统一字段标识，记录预测来源 |
| Prediction Latency | 算法生成预测耗时 | 与 SQL 执行耗时分开 |
| SQL Execution Latency | 数据库执行耗时 | 记录 timeout 和失败情况 |
| Token Usage | 输入/输出 Token | 供应商不提供时标记 unavailable |
| API Cost | API 调用成本 | 仅使用可靠的实际计价信息 |

## 统计约定

- 同时保存样本级结果和数据集级汇总。
- 汇总时明确区分 Macro 与 Micro。
- 对空预测、执行失败、超时和缺失标签制定明确处理规则。
- Spider 2.0 与 CSpider 优先遵循各自官方评测规则。
- 表字段可分别报告算法原生输出和 SQL Parser 提取结果，避免混淆 Schema Linking 与 SQL 解析能力。
