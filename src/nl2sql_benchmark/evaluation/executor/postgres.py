"""PostgreSQL Executor 扩展接口占位；不属于 V1.0 实现范围。"""

from nl2sql_benchmark.core.data import DatabaseRef
from nl2sql_benchmark.core.result import ExecutionResult
from .base import BaseExecutor


class PostgreSQLExecutor(BaseExecutor):
    def execute(self, sql: str, database: DatabaseRef) -> ExecutionResult:
        # TODO: implement in a later version; do not add PostgreSQL dependency in V1.0.
        raise NotImplementedError("TODO: PostgreSQL executor is an extension point")
