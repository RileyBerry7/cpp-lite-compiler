# symbol_table.py

from front_end.ast_node import ASTNode, DeclSpec
from utils.enum_types import *

#############################################################################################################3##########

@dataclass
class Symbol:
    id: int # Unique Identifier
    name:      str          # Identifier Name
    kind:      SymbolKind   # Symbol Role

    # Context
    outer_scope: Scope        # Scope within
    declaration_node: ASTNode # Declaration within

    # Specs
    decl_specs: DeclSpec      # Other specs: qualifiers, base_type...
    storage:    StorageClass  # Linkage Duration: Extern, static...
    func_flags: FuncAttrs     # inline, virtual, noexcept

    # Derived Semantic Info
    is_defined:       bool = True
    # order_index:      int  = -1

    # Source Information
    # loc: None

    # Aggregate Types (Fields): class, struct, enum, union, attributes, methods...
    members: list["Symbol"] | None = None # members within nested scope


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