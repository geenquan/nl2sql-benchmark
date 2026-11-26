"""统一预测结果与执行结果定义。"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PredictionResult:
    """算法统一输出。tables / columns 可以为空。"""

    sample_id: str
    sql: str | None = None
    tables: list[str] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """数据库执行器的统一返回结构。"""

    success: bool
    rows: list[tuple[Any, ...]] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    latency_seconds: float | None = None
    error: str | None = None
    timed_out: bool = False
