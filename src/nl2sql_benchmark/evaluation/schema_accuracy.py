"""Table Precision / Recall / F1 指标占位。"""


class TableAccuracyEvaluator:
    def evaluate(self, predicted_tables: list[str], gold_tables: list[str]) -> dict:
        # TODO: normalize identifiers and implement sample-level / aggregate metrics.
        raise NotImplementedError("TODO: implement table metrics")
