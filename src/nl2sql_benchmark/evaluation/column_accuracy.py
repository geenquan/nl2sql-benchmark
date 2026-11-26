"""Column Precision / Recall / F1 指标占位。"""


class ColumnAccuracyEvaluator:
    def evaluate(self, predicted_columns: list[str], gold_columns: list[str]) -> dict:
        # TODO: normalize identifiers and implement sample-level / aggregate metrics.
        raise NotImplementedError("TODO: implement column metrics")
