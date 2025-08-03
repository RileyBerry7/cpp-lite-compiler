# cst_to_ast.py

from multiprocessing.managers import Token
from typing import Union
from lark import Lark, Transformer, Tree

class node(name):
    def __init__(self, name):
        self.name = name
        self.children = []

class func_def(node):
class type_specifier(node):
class param_list(node):
class param(node):
class stmt(node):
class expr(node):

class assign_stmt(stmt):
class return_stmt(stmt):


class literal_expr(expr):
class id_expr(expr):
class bin_expr(expr):
class un_expr(expr):

    # Transformers work bottom-up (or
    # depth-first), starting with visiting the leaves and working
    # their way up until ending at the root of the tree
    #
    # For each node visited, the transformer will call the
    # appropriate method (callbacks), according to the node's
    # data, and use the returned value to replace the node,
    # thereby creating a new tree structure.
    #
    # Transformers can be used to implement map & reduce
    # patterns. Because nodes are reduced from leaf to root, at
    # any point the callbacks may assume the children have
    # already been transformed (if applicable).
    #
    # If the transformer cannot find a method with the right
    # name, it will instead call __default__, which by default
    # creates a copy of the node.
    #
    # To discard a node, return Discard (lark.visitors.Discard).
    #
    # Transformer can do anything Visitor can do, but because it reconstructs the tree, it is slightly less efficient.
    #
    # A transformer without methods essentially performs a
    # non-memoized partial deepcopy.
    #
    # All these classes implement the transformer interface:
    #
    # Transformer - Recursively transforms the tree. This is the one you probably want.
    # Transformer_InPlace - Non-recursive. Changes the tree in-place instead of returning new instances
    # Transformer_InPlaceRecursive - Recursive. Changes the tree in-place instead of returning new instances

########################################################################################################################
class CSTtoAST(Transformer):
    """
    A Transformer that converts a CST to an AST.
    """

    def __default__(self, data, children, meta):
        """
        Default method for nodes that do not have a specific transformation defined.
        """
        return Tree(data, children, meta)

    ####################################################################################################################
    def translation_unit(self, children):
        return Tree("program", children)

    ####################################################################################################################
    def function_definition(self, children):

        new_children = list()
        new_children.append(children[0]) # return_type
        new_children.append(children[1].children[0]) # function_name
        new_children.append(children[1].children[1]) # function_parameters
        new_children.append(children[2])             # function_body

        return Tree("func_def", new_children)

    ####################################################################################################################
    def type_specifier(self, children):
        return children[0]

    # def declarator(self, children):
    #     return children

    # def parameter_list(self, children):
    #     return Tree("params", [c for c in children if isinstance(c, Tree) and c.data == "parameter"])
    #


