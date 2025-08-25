# declarator_todeclarator_to_symbol.py

from compiler.front_end.symbol_table import Symbol
from compiler.utils.enum_types import SymbolKind, StorageClass
from compiler.front_end.ast_node import *

def declarator_to_symbol(declaration: NormalDeclaration, unique_id: int) -> list[Symbol]:
    """
    Returns a list of Symbol objects.
    """

    decl_specs    = declaration.decl_specs
    decl_list     = declaration.decl_list
    is_func_def   = True if declaration.func_body else False
    built_symbols = []

    if is_func_def:
        print()
        # Return path for Function Definition

    # Loop through and Build Symbol for Every Declarator
    for declarator in decl_list:

        ################################################################################################################
        # Build Symbol
        id        = unique_id
        name      = declarator.decl_name
        kind      = SymbolKind.Var

        # Declaration Context
        scope     = None
        declaration_node = declaration

        # Declaration Specifications
        decl_spec = decl_specs

        # Semantic Information
        storage    = StorageClass[decl_spec.storage_class.upper()]
        func_flags: FuncAttrs
        is_defined: bool = False
        order_index: int = -1

        # Source Information
        # loc: None

        # Aggregate Information
        members: list[None] = None  # Structs / Enums

        ################################################################################################################

        # Construct / Push Symbol
        curr_symbol = Symbol(id, name, kind, scope, declaration_node, decl_specs, storage,
                             func_flags, is_defined, order_index, members)
        built_symbols.append(curr_symbol)


    return built_symbols
