# enum_types.py

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


#############################################################################################################3##########

class ScopeKind(Enum):
    GLOBAL    = auto() # Global scope for a file
    NAMESPACE = auto() # Namespace body
    FUNCTION  = auto() # Function body
    BLOCK     = auto() # Control-flow body (if, else, while)
    CLASS     = auto() # class/struct/union body
    ENUM      = auto() # Enum body
    LAMBDA    = auto() # ???

#############################################################################################################3##########

class SymbolKind(Enum):
    Var       = auto()   # default variable declaration
    Param     = auto()   # Parameter within function suffix
    Func      = auto()   # function declaration
    Field     = auto()   # data-member declared in a class/struc/enum
    Label     = auto()   # Label declaration
    TypeAlias = auto()   # typedef / using
    Class     = auto()   # Class Declaration
    Struct    = auto()   # Struct Declaration
    Union     = auto()   # Union Declaration
    Enum      = auto()   # Enum Declaration

class StorageClass(Enum):
    None_       = auto()
    Static      = auto()
    Extern      = auto()

@dataclass
class FuncAttrs:
    inline   : bool = False
    noexcept : bool = False
    explicit : bool = False
    virtual  : bool = False
    override : bool = False
    final    : bool = False

# @dataclass(frozen=True)
# class SourceLoc:
#     file: str
#     line: int
#     col: int

#############################################################################################################3##########
class ElaboratedTypeKind(Enum):
    CLASS    = auto() # class / struct
    ENUM     = auto() # enum
    UNION    = auto() # union
#############################################################################################################3##########
# Used for
class AccessType(Enum):
    PRIVATE   = auto()
    PUBLIC    = auto()
    PROTECTED = auto()