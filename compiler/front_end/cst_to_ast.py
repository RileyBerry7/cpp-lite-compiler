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
        parameter_node = parameter(children[0], children[1])
        return parameter_node

    ####################################################################################################################
    def function_suffix(self, children):
        params = []

        # Gather children
        # for child in children:
        #     params.append(child)
        # param_list_node = parameter_list(children, params)

        return ASTNode("parameter_list", children)