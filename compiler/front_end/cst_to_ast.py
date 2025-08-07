# cst_to_ast.py

from lark import Lark, Transformer, Tree
from compiler.front_end.ast_node import *

VALID_TYPE_SETS = {
        frozenset(['void']),
        frozenset(['bool']),
        frozenset(['char']),
        frozenset(['signed']),
        frozenset(['signed', 'char']),
        frozenset(['unsigned']),
        frozenset(['unsigned', 'char']),
        frozenset(['int']),
        frozenset(['signed', 'int']),
        frozenset(['unsigned', 'int']),
        frozenset(['short']),
        frozenset(['short', 'int']),
        frozenset(['signed', 'short']),
        frozenset(['signed', 'short', 'int']),
        frozenset(['unsigned', 'short']),
        frozenset(['unsigned', 'short', 'int']),
        frozenset(['long']),
        frozenset(['long', 'int']),
        frozenset(['long', 'long']),
        frozenset(['long', 'long', 'int']),
        frozenset(['signed', 'long']),
        frozenset(['signed', 'long', 'int']),
        frozenset(['signed', 'long', 'long']),
        frozenset(['signed', 'long', 'long', 'int']),
        frozenset(['unsigned', 'long']),
        frozenset(['unsigned', 'long', 'int']),
        frozenset(['unsigned', 'long', 'long']),
        frozenset(['unsigned', 'long', 'long', 'int']),
        frozenset(['float']),
        frozenset(['double']),
        frozenset(['long', 'double']),
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
        return ASTNode(token.value)

    ####################################################################################################################
    def parameter(self, children):
        parameter_node = Parameter(children[0], children[1])
        return parameter_node

    ####################################################################################################################
    def declaration_specifier_list(self, children):
        simple_types  = []
        qualifiers    = []
        storage_class = []

        # Determine Children Types
        if children:
            for child in children:
                if isinstance(child, ASTNode):
                    if child.name == "simple_type_specifier":
                        simple_types.append(child.children[0].name)
                        print("############################################################### Found Simple Type Secifier ####################")
                    elif child.name == "type_qualifier":
                        qualifiers.append(child.children[0].name)
                    elif child.name == "storage_class_specifier":
                        storage_class.append(child.children[0].name)
                elif isinstance(child, Tree):
                    if child.name == "simple_type_specifier":
                        simple_types.append(child.children[0].value)


        # ERROR CHECKING
        types_found = frozenset(simple_types)
        if types_found in VALID_TYPE_SETS:
            # Grab Base Type
            base_type = "int"

            # Check If Unsigned
            is_signed = True

            # Calculate Size
            size = 32

            # Compile Type Node
            type_node = Type(' '.join(sorted(types_found)), base_type, size, is_signed)

        # ERROR: Invalid Type Found
        else:
            return Error("Invalid type specifier found.")

        # Create and Return Declaration Specifier Node
        specifier_node = DeclSpec(type_node, qualifiers, storage_class)
        return specifier_node

    ####################################################################################################################

    ####################################################################################################################
    # Expression Precedence Abstraction

    def primary(self, children):
        if children and len(children) == 1:
            return children[0]
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
    ####################################################################################################################

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
