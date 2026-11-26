"""SQLite Executor 占位；SQLite 是 V1.0 首期执行目标。"""

from nl2sql_benchmark.core.data import DatabaseRef
from nl2sql_benchmark.core.result import ExecutionResult
from .base import BaseExecutor


class SQLiteExecutor(BaseExecutor):
    def execute(self, sql: str, database: DatabaseRef) -> ExecutionResult:
        # TODO: implement sqlite3 connection, read-only mode, timeout/progress handler,
        # error capture, result normalization, and resource cleanup.
        raise NotImplementedError("TODO: implement SQLite execution")
