"""CSpider 中文数据集适配器占位。"""

from collections.abc import Iterable

from nl2sql_benchmark.core.data import DatasetSample
from .base import BaseDataset


class CSpiderDataset(BaseDataset):
    def load(self) -> Iterable[DatasetSample]:
        # TODO: inspect local CSpider release layout and split definitions.
        # TODO: normalize Chinese questions, SQLite schema, gold SQL and database refs.
        raise NotImplementedError("TODO: implement CSpider loader")
