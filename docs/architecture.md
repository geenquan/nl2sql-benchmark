# 架构说明

## 调用方向

`Dataset -> InputData -> BaseNL2SQL.predict() -> PredictionResult -> PredictionStore -> Evaluator -> Report`

Gold 标签和数据库引用由 Dataset / Runner 保管，不传给算法。算法只生成预测，不执行 SQL、不计算指标。

## 关键边界

- `core` 只定义协议，不依赖具体算法和数据集。
- `datasets` 负责数据格式转换，不负责模型调用。
- `methods` 负责把具体产品/项目/论文方法适配为统一预测接口。
- `evaluation` 负责执行和评价，不调用模型。
- `storage` 负责保存预测与运行元数据。
- `common` 提供可选工具，不要求每种算法使用。

## 运行与重评估

一次实验分为两个逻辑阶段：

1. Predict：调用算法并逐样本持久化原始预测。
2. Evaluate：读取已保存预测和 Gold 标签，执行 SQL、计算指标、生成报告。

重评估只运行第二阶段。
