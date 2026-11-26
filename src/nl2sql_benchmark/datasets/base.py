"""数据集适配器基类。"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from nl2sql_benchmark.core.data import DatasetSample


class BaseDataset(ABC):
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    @abstractmethod
    def load(self) -> Iterable[DatasetSample]:
        """加载统一 DatasetSample；Gold 信息不得放入 input_data。"""
        raise NotImplementedError("TODO: implement dataset loading")
