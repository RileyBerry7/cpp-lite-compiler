from multiprocessing.managers import Token

from lark import Tree


########################################################################################################################
class DecNode:
    """
    Short for Decorated Node, this class represents a tree node which we will use to fully rebuild and replace our AST's
    current structure. The primary difference in this class is that it has a special attribute dedicated to storing
    semantic information relevant to the LLVM IR generation process or "decorations".
    """
    def __init__(self, node_name=None):

        # Abstract Node Details
        self.name = node_name
        self.children = []

        # Semantic Details (for LLVM IR)
        self.decorations = {}

########################################################################################################################
class ASTtoDAST:
    """
    A class that will decorate the AST with LLVM IR relevant semantic information. The decoration process will
    recursively travers the AST and fully create a decorated version of it using the DecNode class instead of
    the lark tree class.
    """
    def __init__(self):
        print()

    ####################################################################################################################
    def decorate(self, cst: Tree) -> DecNode\

        # Create: D-AST Root
        dast_root = DecNode(cst.data)

        # DFS Traversal
        dfs(cst)

        # Return: D-AST Root
        return  dast_root


    ####################################################################################################################
    def dfs(self, node):

        # Check If Token
        if isinstance(node, Token):
            print()

        # Check If Lark Tree Node
        elif isinstance(node, Tree):

            # Loop through all children
            for child in node.children:
                if isinstance(child, Tree) and child.data = "func_def":

# END: class ASTtoDAST:
########################################################################################################################