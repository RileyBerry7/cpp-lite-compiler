# error_table.py

from enum import Enum, auto
from dataclasses import dataclass
from compiler.utils.data_classes import SourceLocation

####################################################################################################################
class Severity(Enum):
    ERROR   = auto()
    WARNING = auto()
    NOTE    = auto()

####################################################################################################################

class ErrorKind(Enum):
    REDECLARATION           = auto() # Name redefined in same scope
    UNDECLARED_IDENTIFIER   = auto() # Use of undeclared variable/function
    CONFLICTING_DECLARATION = auto() # Same name, incompatible types/signatures
    AMBIGUOUS_REFERENCE     = auto() # Multiple visible matches, cannot resolve
    ILLEGAL_SHADOWING       = auto() # Inner declaration hides outer (warn/error)
    ACCESS_VIOLATION        = auto() # Invalid access (private/protected)
    NAMESPACE_MEMBER_MISSING= auto() # No such member in namespace/qualifier
    INCOMPLETE_TYPE_USE     = auto() # Forward-declared/incomplete type used illegally
    INVALID_STATIC_CONTEXT  = auto() # Use of non-static member without `this`

####################################################################################################################

# Message catalog
MESSAGE_TEMPLATES = {
    ErrorKind.REDECLARATION: "Redeclaration of '{name}'",
    ErrorKind.UNDECLARED_IDENTIFIER: "Use of undeclared identifier '{name}'",
    # ErrorKind.TYPE_MISMATCH: "Incompatible types: {lhs} vs {rhs}",
}
####################################################################################################################

# Diagnostic Entry
@dataclass
class Diagnostic:
    severity: Severity
    kind: ErrorKind
    loc: tuple[str, int, int]  # (filename, line, col)
    args: dict                 # e.g., {"lhs": "int", "rhs": "float"}

####################################################################################################################
class DiagnosticEngine:
    def __init__(self):
        self.entries: list[Diagnostic] = []

    def report(self, kind: ErrorKind, severity: Severity, loc, **kwargs):
        self.entries.append(Diagnostic(severity, kind, loc, kwargs))

    def dump(self):
        for diag in self.entries:
            template = MESSAGE_TEMPLATES[diag.kind]
            msg = template.format(**diag.args)
            file, line, col = diag.loc
            print(f"{file}:{line}:{col}: {diag.severity.name.lower()}: {msg}")

####################################################################################################################