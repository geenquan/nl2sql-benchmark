"""统一数据库执行器接口。"""

from abc import ABC, abstractmethod

from nl2sql_benchmark.core.data import DatabaseRef
from nl2sql_benchmark.core.result import ExecutionResult


class BaseExecutor(ABC):
    @abstractmethod
    def execute(self, sql: str, database: DatabaseRef) -> ExecutionResult:
        """在指定数据库执行 SQL，返回统一结果。"""
        raise NotImplementedError("TODO: implement execute()")

    def close(self) -> None:
        # TODO: close pooled connections / cursors when applicable.
        return None
