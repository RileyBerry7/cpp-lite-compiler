# declarator_todeclarator_to_symbol.py

from compiler.front_end.symbol_table import Symbol
from compiler.utils.enum_types import SymbolKind

def declarator_to_symbol(decl_list, declarator, unique_id: int) -> Symbol:
    """
    Convert a declarator in a declaration list to a symbol.
    """

    # Build Symbol
    id     = unique_id
    name: str  # Identifier Name
    kind: SymbolKind
    namespace: NamespaceKind

    # Declaration Context
    scope: Scope
    declaration_node: ASTNode

    # Declaration Specifications
    decl_specs: DeclSpec

    # Semantic Information
    storage: StorageClass
    func_flags: FuncAttrs
    is_defined: bool = False
    order_index: int = -1

    # Source Information
    # loc: None

    # Aggregate Information
    members: list[None] = None  # Structs / Enums

    # Determine Symbol Kind and Namespace


    return symbol