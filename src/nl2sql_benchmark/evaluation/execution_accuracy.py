"""SQL 执行成功率与执行结果准确率占位。"""


class ExecutionAccuracyEvaluator:
    def evaluate(self, prediction_result, gold_result) -> dict:
        # TODO: define ordered/unordered comparison and dataset-specific result semantics.
        raise NotImplementedError("TODO: implement execution metrics")
