# declarator_todeclarator_to_symbol.py

from compiler.front_end.symbol_table import Symbol
from compiler.utils.enum_types import *
from compiler.front_end.ast_node import *

def declarator_to_symbol(current_scope:Scope, declaration: NormalDeclaration, unique_id: int) -> list[Symbol]:
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

        # Semantic Information

        # Resolve: Storage Class
        if decl_specs.storage_class and StorageClass.__members__.get(decl_spec.storage_class.upper(), None):
            storage = StorageClass[decl_spec.storage_class.upper()]
        else:
            storage = StorageClass.None_

        # Resolve: Function Specifiers
        func_flags = FuncAttrs()
        if "inline" in decl_specs.func_specifier_set:
            func_flags.inline = True
        if "noexcept" in decl_specs.func_specifier_set:
            func_flags.noexcept = True
        if "explicit" in decl_specs.func_specifier_set:
            func_flags.explicit = True
        if "virtual" in decl_specs.func_specifier_set:
            func_flags.virtual = True
        if "override" in decl_specs.func_specifier_set:
            func_flags.override = True
        if "final" in decl_specs.func_specifier_set:
            func_flags.final = True

        # Resolve: is_defined
        is_defined: bool = True


        # order_index: int = -1

        # Source Information
        # loc: None

        # Resolve Members (Fields): class, struct, enum, union, attributes, methods...
        members = [] # members within nested scope

        ################################################################################################################

        # Construct / Push Symbol
        curr_symbol = Symbol(id, name, kind, scope, declaration_node, decl_specs, storage,
                             func_flags, is_defined, members)
        built_symbols.append(curr_symbol)


    return built_symbols
