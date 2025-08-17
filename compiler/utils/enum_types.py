# enum_types.py

from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal, Union


#############################################################################################################3##########

class ScopeKind(Enum):
    File      = auto()  # Global scope for a file
    Function  = auto()  # Function scope
    Block     = auto()  # Block scope (e.g., inside if, for, etc.)
    Struct    = auto()  # Struct/Union scope
    Enum      = auto()  # Enum scope

class Scope:
    def __init__(self, kind: ScopeKind, parent: "Scope" = None):
        self.kind   = ScopeKind
        self.parent = parent  # Scope which contains this scope (Outer Scope)
        self.symbols = {}     # name -> Symbol

class SymbolKind(Enum):
    Var       = auto()
    Param     = auto()
    Func      = auto()
    TypeAlias = auto()     # typedef / using
    StructTag = auto()
    EnumTag   = auto()
    Field     = auto()
    Label     = auto()

class NamespaceKind(Enum):
    Ordinary = auto()      # variables, functions, params
    Tag      = auto()      # struct/union/enum tags
    Type     = auto()      # typedef/using names
    LabelNS  = auto()      # goto labels (function scope)

class StorageClass(Enum):
    None_    = auto()
    Auto     = auto()
    Static   = auto()
    Extern   = auto()
    Typedef  = auto()

@dataclass
class FuncAttrs:
    inline: bool    = False
    constexpr: bool = False
    consteval: bool = False
    noexcept: bool  = False
    explicit: bool  = False
    virtual: bool   = False
    override: bool  = False
    final: bool     = False

# @dataclass(frozen=True)
# class SourceLoc:
#     file: str
#     line: int
#     col: int

#############################################################################################################3##########
