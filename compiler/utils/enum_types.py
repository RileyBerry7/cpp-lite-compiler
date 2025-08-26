# enum_types.py

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


#############################################################################################################3##########

class ScopeKind(Enum):
    File      = auto()  # Global scope for a file
    Function  = auto()  # Function scope
    Block     = auto()  # Block scope (e.g., inside if, for, etc.)

    #
    Class     = auto()
    Struct    = auto()  # Struct/Union scope
    Enum      = auto()  # Enum scope

class Scope:
    def __init__(self, kind: ScopeKind, scope_id:int, parent: "Scope" | None = None):
        self.kind    = ScopeKind
        self.id      = scope_id
        self.parent  = parent  or None # Scope which contains this scope (Outer Scope)
        self.symbols = {}              # Dict of {symbol_name: symbol_id}

class ScopeStack:
    def __init__(self):
        self.scopes = []
        self.next_id = 0  # Unique identifier for symbols
        self.curr_scope = Scope(ScopeKind.File, self.next_id, None)

        # Initial Scope
        self.scopes.append(self.curr_scope)

    def enter_scope(self, scope_kind:str):

        self.next_id += 1 # Increment ID

        # Create New Scope
        new_scope = Scope(ScopeKind[scope_kind.upper()], self.next_id, self.curr_scope)
        self.scopes.append(new_scope)  # Push to Scope Stack
        self.curr_scope = new_scope    # Update Current Scope


    # def exit_scope(self):

    # def resolve_scope(self):




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