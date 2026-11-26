"""所有 NL2SQL 方法的统一基类。"""

from abc import ABC, abstractmethod
from typing import Any

from .data import InputData
from .result import PredictionResult


class BaseNL2SQL(ABC):
    """算法适配器只负责预测，不负责 SQL 执行和指标评估。"""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    @abstractmethod
    def predict(self, input_data: InputData) -> PredictionResult:
        """根据统一输入生成 SQL 和可选的表/字段预测。"""
        raise NotImplementedError("TODO: implement predict() in each method adapter")

    def close(self) -> None:
        """释放模型、HTTP 客户端或外部服务资源（如有）。"""
        # TODO: implement resource cleanup when needed.
        return None
