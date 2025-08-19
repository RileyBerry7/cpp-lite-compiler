# symbol_table.py

from dataclasses import dataclass, field
from compiler.front_end.ast_node import ASTNode, DeclSpec
from compiler.utils.enum_types import *

#############################################################################################################3##########

@dataclass
class Symbol:
    id: int # Unique Identifier
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
        self.symbols: {Symbol}     = {} # Symbol Table
        self.next_id: int          = 0

    def insert_symbol(self, symbol: Symbol):

        self.next_id += 1  # Increment ID

        symbol.id = self.next_id         # Bind Symbol to Unique ID
        self.symbols[symbol.id] = symbol # Insert Symbol into Table via ID

        # Return Unique ID
        return symbol.id

#############################################################################################################3##########