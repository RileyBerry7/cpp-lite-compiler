# cst_to_ast.py
from multiprocessing.managers import Token
from typing import Union

from lark import Lark, Transformer, Tree

def dfs(node: Union[Token, Tree]):
    """"  """
    if isinstance(node, Token):
        print("Token:", node.id)
        return
    elif isinstance(node, Tree):
        print("Node:", node.data)
        for child in node.children:
            dfs(child)

def transform(cst: Tree) -> Tree:

    # Use Recursion to traverse the list
    dfs(cst)
    print("\033[91mRecursive_DFS: Finished\033[0m")
    return cst

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

