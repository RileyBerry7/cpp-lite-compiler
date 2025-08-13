# cst_to_ast.py
from multiprocessing.managers import Token

from lark import Lark, Transformer, Tree
from compiler.front_end.ast_node import *
from compiler.utils.literal_kind import *
from compiler.utils.lexeme_to_number import lexeme_to_number
from compiler.utils.scalar_size import scalar_size

BASE_TYPES = {'void', 'bool', 'char', 'signed', 'unsigned', 'int', 'float'}

VALID_TYPE_SETS = {
    ('void',),
    ('bool',),
    ('char',),
    ('signed',),
    ('char', 'signed'),
    ('unsigned',),
    ('char', 'unsigned'),
    ('int',),
    ('int', 'signed'),
    ('int', 'unsigned'),
    ('short',),
    ('int', 'short'),
    ('short', 'signed'),
    ('int', 'short', 'signed'),
    ('short', 'unsigned'),
    ('int', 'short', 'unsigned'),
    ('long',),
    ('int', 'long'),
    ('long', 'long'),
    ('int', 'long', 'long'),
    ('long', 'signed'),
    ('int', 'long', 'signed'),
    ('long', 'long', 'signed'),
    ('int', 'long', 'long', 'signed'),
    ('long', 'unsigned'),
    ('int', 'long', 'unsigned'),
    ('long', 'long', 'unsigned'),
    ('int', 'long', 'long', 'unsigned'),
    ('float',),
    ('double',),
    ('double', 'long'),
}

########################################################################################################################
class CSTtoAST(Transformer):
    """
    A Transformer that converts a CST to an AST.
    """

    def __default__(self, data, children, meta):
        abstract_node = ASTNode(data, children)
        return abstract_node

    def __default_token__(self, token):

        return ASTNode(token.value, [ASTNode(token.type)])

    ####################################################################################################################
    def declaration_specifier_list(self, children):

        # Initialize Empty Specs
        simple_types       = []
        elaborate_types    = []
        elaborate_name     = None
        qualifier          = None
        storage_class      = None
        function_specifier = None

        ################################################################################################################
        # Determine Children Names
        if children:
            for child in children:
                if isinstance(child, ASTNode):

                    # FOUND: Simple Type Specifier
                    if child.name == "simple_type_specifier":
                        simple_types.append(child.children[0].name)

                    # FOUND: Elaborate Type Specifier
                    elif child.name == "elaborated_type_specifier":

                        # SEMANTIC ERROR: multiple non-duplicate elaborate type names
                        if elaborate_name is not None and child.children[1].name == elaborate_name:
                            return Error("Multiple non-duplicate elaborate type names")
                        else:
                            # SAVE: Elaborate Type & Name
                            elaborate_type = child.children[0].name
                            elaborate_name = child.children[1].name

                    # FOUND: Type Qualifier
                    elif child.name == "type_qualifier":
                        # SEMANTIC ERROR: multiple type qualifiers
                        if qualifier is not None:
                            return Error("Multiple type qualifiers found")
                        qualifier = child.children[0].name

                    # Found: Storage Class Specifier
                    elif child.name == "storage_class_specifier":
                        # SEMANTIC ERROR: multiple storage class specifiers
                        if storage_class is not None:
                            return Error("Multiple storage class specifiers found")
                        storage_class = child.children[0].name

                    # Found: Function Specifier
                    elif child.name == "function_specifier":
                        function_specifier = child.children[0].name

        # END - Determine Children Names
        ################################################################################################################

        # SEMANTIC ERROR: mutual exclusivity of simple_type & elaborate_type
        if elaborate_types and simple_types:
            return Error("'Elaborate' and 'Simple' types are mutually exclusive")

        # ERROR CHECKING: base_type / is_signed
        types_found = tuple(sorted(simple_types))
        if types_found in VALID_TYPE_SETS:

            # Grab base type
            if elaborate_name is not None:
                # Identifier Type Name
                base_type = elaborate_name
            else:
                # Simple Type Name
                base_type = next((t for t in types_found if t in BASE_TYPES), None)

            # Check If Unsigned
            is_signed = True
            for elem in types_found:
                if elem == "unsigned":
                    is_signed = False
                    break

            # Calculate Size
            if elaborate_types:
                size = None
                print("\033[93;5;28mWarning: Found elaborate type, memory size uncertain.\n"
                      + str(elaborate_types) + "\033[0m")
            else:
                size = scalar_size(types_found, base_type, "LLP64")

            # Compile Type Node
            type_node = Type(' '.join(types_found), base_type, size, is_signed, elaborate_types)

        # ERROR: Found Type Not in Valid Set
        else:
            return Error("Invalid type specifier found.")

        # Create and Return Declaration Specifier Node
        specifier_node = DeclSpec(type_node, qualifier, storage_class, function_specifier)
        return specifier_node


    ####################################################################################################################
    # Expression Precedence Abstraction
    def primary(self, children):
        if children and len(children) == 1:
            if isinstance(children[0], ASTNode) and children[0].name == "literal":
                literal_type = token_to_literal_kind(children[0].children[0].children[0].name)
                literal_value =  lexeme_to_number(children[0].children[0].name)
                return LiteralExpr(literal_type, literal_value)

            else:
                return ASTNode("primary", children)

    def unary(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("unary", children)

    def postfix(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("postfix", children)

    def product(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("product", children)


    def sum(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("sum", children)
    def relational(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("relational", children)
    def equality(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("equality", children)
    def logic_and(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("logic_and", children)
    def logic_or(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("logic_or", children)
    def conditional_expression(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("conditional_expression", children)

    def assignment_expression(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("assignment_expression", children)

    ################

    # def literal(self, children):

    ####################################################################################################################
    # This does not handle direct declarator unbinding yet
    # def direct_declarator(self, children):
    #     if children and len(children) == 1:
    #         return DeclName(children[0].name)
    #     else:
    #         return ASTNode("direct_decl", children)


    # def pointer(self, children):
    #     # Check if has children
    #     if children:
    #         if isinstance(children[0], ASTNode):
    #             # Grab Reference Type
    #             reference_type = ReferenceType(children[0].name)
    #
    #         # Grab Remaining Qualifiers If Any
    #         qualifiers = []
    #         for child in children[1:]:
    #             if isinstance(child, ASTNode):
    #                 qualifiers.append(child.name)
    #
    #     new_chain = PointerChain(reference_type, qualifiers)
    #
    #     return PointerChain(children)
    #
    #
    #     if children:
    #         for child in children:
    #             if isinstance(child, PointerChain):
    #
    #     chain = []
    #     for child in children:
    #         if isinstance(child, PointerChain):
    #                 new_chain.append_chain(child)

    ####################################################################################################################
    # def function_suffix(self, children):
    #     params = []
    #
    #     # Gather children
    #     # for child in children:
    #     #     params.append(child)
    #     # param_list_node = parameter_list(children, params)
    #
    #     return ASTNode("parameter_list", children)

    ####################################################################################################################
    # PTR -> POINTER LEVEL
    def ptr(self, children):

        # Initialize Empty Lists
        scope_path      = []
        type_qualifiers = []

        # Early Return: only child = plain '*'
        if len(children) == 1:
            return PtrLevel()

        # Check For: Scope_Qualifier Child
        elif isinstance(children[0], ASTNode) and children[0].name == "scope_qualifier":
            for grandchild in children[0].children:
                if grandchild != "::":
                    scope_path.append(grandchild.name)

        # Check For: Type_Qualifier Children @ [1]
        if len(children) >= 2 and isinstance(children[1], ASTNode) and children[1].name == "type_qualifier_list":
            for grandchild in children[1].children:
                type_qualifiers.append(grandchild.name)

        # Check For: Type_Qualifier Children @ [3]
        elif len(children) >= 4 and isinstance(children[3], ASTNode) and children[3].name == "type_qualifier_list":
            for grandchild in children[3].children:
                type_qualifiers.append(grandchild.name)

        # Declare and Return PtrLevel Object
        return PtrLevel(scope_path, type_qualifiers)



    ####################################################################################################################
