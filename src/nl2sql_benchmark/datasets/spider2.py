"""Spider 2.0 数据集适配器占位。

V1.0 首期只支持 SQLite 方言任务。其他方言任务必须显式跳过并记录原因，
不得静默转换 SQL 或伪装成 SQLite 任务。
"""

from collections.abc import Iterable

from nl2sql_benchmark.core.data import DatasetSample
from .base import BaseDataset


class Spider2Dataset(BaseDataset):
    def load(self) -> Iterable[DatasetSample]:
        # TODO: inspect the selected Spider 2.0 release layout and task manifest.
        # TODO: select SQLite tasks only and report unsupported task counts/reasons.
        # TODO: normalize question, schema, gold labels, and database references.
        raise NotImplementedError("TODO: implement Spider 2.0 SQLite subset loader")
