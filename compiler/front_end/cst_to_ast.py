# cst_to_ast.py

from lark import Lark, Transformer, Tree
from compiler.front_end.ast_node import *

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
        base_type     = []
        qualifiers    = []
        storage_class = []

        # Determine Children Types
        if children:
            for child in children:
                if isinstance(child, ASTNode):
                    if child.name == "type_specifier":
                        base_type.append(child.children[0])
                    elif child.name == "type_qualifier":
                        qualifiers.append(child.children[0])
                    elif child.name == "storage_class_specifier":
                        storage_class.append(child.children[0])


        # ERROR CHECKING
        if len(base_type) > 2: # Too many base_types
            print("\033[91mError: Multiple base types found.\033[0m")
            return Error("Type Error")

        elif len(base_type) == 2: # base_type + modifier
            print()

        elif len(base_type) == 1: # Single base_type
            base_type = base_type[0]

        else: # No base type
            print("\033[91mError: Base type not found.\033[0m")
            return Error("Type Error")

        # Create and Return Declaration Specifier Node
        specifier_node = DeclSpec(base_type, qualifiers, storage_class)
        return specifier_node


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
