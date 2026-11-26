"""性能、Token 和成本统计占位。"""


class PerformanceEvaluator:
    def evaluate(self, prediction_records: list[dict]) -> dict:
        # TODO: separate model prediction latency from SQL execution latency.
        # TODO: report mean, median, P95, timeout rate, token usage and optional API cost.
        raise NotImplementedError("TODO: implement performance metrics")
