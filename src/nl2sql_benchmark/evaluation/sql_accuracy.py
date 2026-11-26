"""SQL Exact Match / Validity 指标占位。"""


class SQLAccuracyEvaluator:
    def evaluate(self, prediction_sql: str | None, gold_sql: str, dialect: str) -> dict:
        # TODO: delegate to the dataset's official evaluation rules where available.
        raise NotImplementedError("TODO: implement SQL accuracy metrics")
