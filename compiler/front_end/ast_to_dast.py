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

    ####################################################################################################################
    def pretty(self):
        """ Returns a string visualizing the subtree rooted at this node."""

        text_tree  = self.name + "\n"
        text_tree += self.walk(self, 1)

        return text_tree

    def walk(self, node, curr_indent):
        text_tree = ""

        if node.children:
            for child in node.children:
                text_tree += curr_indent*"  " + child.name + "\n"
                text_tree += self.walk(child, curr_indent+1)
        # else:
            # text_tree = (curr_indent+1)*"  " + "[No children]\n"

        return text_tree

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
    def decorate(self, ast: Tree) -> DecNode:

        # Create: D-AST Root
        dast_root = DecNode(ast.data)

        # DFS Traversal
        dast_root.children = self.dfs(ast)

        # Return: D-AST Root
        return  dast_root


    ####################################################################################################################
    def dfs(self, node) -> [DecNode]:

        # Initialize: Return Variable
        decorated_children = []

        # Check If Token
        if isinstance(node, Token):
            print()

        # Check If Lark Tree Node
        elif isinstance(node, Tree):
            # Loop through all children
            for child in node.children:
                if isinstance(child, Tree) and child.data == "func_def":

                    # Build Child Node
                    temp_node = DecNode(child.data)
                    temp_node.children = self.dfs(child)

                    # Push Child to List
                    decorated_children.append(temp_node)

        # Return: List of Decorated Nodes
        return decorated_children

# END: class ASTtoDAST:
########################################################################################################################