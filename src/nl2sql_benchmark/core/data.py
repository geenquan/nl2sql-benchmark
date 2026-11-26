"""统一输入与数据集内部对象定义。

TODO: 在数据集 Loader 开发阶段补充严格校验、标准化和序列化。
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InputData:
    """算法可见的最小输入；不得包含 Gold 标签或数据库凭据。"""

    sample_id: str
    question: str
    schema: dict[str, Any]
    dialect: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class GoldData:
    """仅供 Runner / Evaluator 使用，不得传入算法。"""

    sample_id: str
    gold_sql: str | None = None
    gold_tables: list[str] = field(default_factory=list)
    gold_columns: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class DatabaseRef:
    """数据库引用；不包含明文密码或其他秘密。"""

    database_id: str
    dialect: str
    path: str | None = None
    connection_name: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class DatasetSample:
    """框架内部样本：算法输入、Gold 标签和数据库引用相互隔离。"""

    input_data: InputData
    gold: GoldData
    database: DatabaseRef
