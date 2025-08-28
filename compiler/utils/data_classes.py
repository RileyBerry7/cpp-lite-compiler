# data_classes.py

from dataclasses import dataclass

@dataclass
class SourceLocation:
    filename: str
    line: int
    column: int
    span: tuple[int, int] | None = None   # optional (start, end char positions)
