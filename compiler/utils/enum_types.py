# enum_types.py

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto, unique


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
#############################################################################################################3##########

@unique
class LiteralKind(str, Enum):
    INT     = "INT"
    FLOAT   = "FLOAT"
    CHAR    = "CHAR"
    STRING  = "STRING"
    BOOL    = "BOOL"
    NULLPTR = "NULLPTR"

def get_kind(raw_token: str):
    if raw_token == "INT_LITERAL":
        return LiteralKind.INT
    elif  raw_token == "FLOAT_LITERAL":
        return LiteralKind.FLOAT
    elif  raw_token == "STRING_LITERAL":
        return LiteralKind.STRING
    elif  raw_token == "CHAR_LITERAL":
        return LiteralKind.CHAR
    elif  raw_token == "BOOL_LITERAL":
        return LiteralKind.BOOL
    elif  raw_token == "NULLPTR_LITERAL":
        return LiteralKind.NULLPTR
#############################################################################################################3##########
