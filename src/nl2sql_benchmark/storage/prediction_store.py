"""原始预测 JSONL 存储接口占位。"""

from nl2sql_benchmark.core.result import PredictionResult


class PredictionStore:
    def append(self, result: PredictionResult) -> None:
        # TODO: append one JSON object per line; never overwrite an existing run.
        raise NotImplementedError("TODO: implement JSONL append")

    def read(self):
        # TODO: stream PredictionResult records from JSONL.
        raise NotImplementedError("TODO: implement JSONL read")
