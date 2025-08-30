from __future__ import annotations

from compiler.utils.colors import colors
from compiler.utils.data_classes import SourceLocation


class ASTNode:
    """ Represents a node in the Abstract Syntax Tree (AST)."""

    def __init__(self, node_name=None, children:list[ASTNode] | None=None):

        # Abstract Node Details
        self.name     = node_name
        self.children = children or []
        self.loc      = SourceLocation

        # Pretty Printing Details
        self.ansi_color: colors = colors.white

    ####################################################################################################################
    def pretty(self):
        """ Returns a string visualizing the subtree rooted at this node."""

        text_tree  = self.ansi_color(self.name) + "\n"
        text_tree += self.walk(self, 1)

        return text_tree

    def walk(self, node, curr_indent):
        text_tree = ""

        if node.children:
            for child in node.children:
                text_tree += curr_indent*"  " + child.ansi_color(child.name) + "\n"
                text_tree += self.walk(child, curr_indent+1)
        # else:
            # text_tree = (curr_indent+1)*"  " + "[No children]\n"

        return text_tree
########################################################################################################################
    def dfs(self, visit):

        visit(self) # Call Visit Function

        # Recursively Walk Children
        for child in self.children:
            child.dfs(visit)

    ########################################################################################################################
