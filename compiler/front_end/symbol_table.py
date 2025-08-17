# symbol_table.py

from dataclasses import dataclass, field
from compiler.front_end.ast_node import ASTNode, DeclSpec
from compiler.utils.enum_types import *

#############################################################################################################3##########

@dataclass
class Symbol:
    name:      str # Identifier Name
    kind:      SymbolKind
    namespace: NamespaceKind

    # Declaration Context
    scope: Scope
    declaration_node: ASTNode

    # Declaration Specifications
    decl_specs: DeclSpec

    # Semantic Information
    storage:     StorageClass
    func_flags:  FuncAttrs
    is_defined:  bool = False
    order_index: int  = -1

    # Source Information
    # loc: None

    # Aggregate Information
    members: list[None] = None # Structs / Enums


#############################################################################################################3##########

class SymbolTable:
    def __init__(self):
        self.scopes:  list[Scope]  = []  # Scope Stack
        self.symbols: list[Symbol] = [] # Symbol Table

    def insert_symbol(self, symbol: Symbol):
        print()

#############################################################################################################3##########