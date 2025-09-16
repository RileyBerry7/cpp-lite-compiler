from compiler.front_end.abstract_nodes.ast_node import ASTNode
from compiler.front_end.decorator import Decorator
from compiler.utils.colors import colors

class Disambiguator(Decorator):

    def IDENTIFIER(self, node:ASTNode, children: list[ASTNode]):
        if children[0].name in keywords:
            node.name = "DeadBranch"
            node.ansi_color = colors.red
            children.pop()

    # def __default__(self, node:ASTNode, children: list[ASTNode]):
    #     for child in children:
    #         if child.name == "DeadBranch":
    #             node = child

    # def Ambiguity(self, node:ASTNode, children: list[ASTNode]):
        # for index, ambig_branch in enumerate(children):
        #     if ambig_branch.name == "DeadBranch":
        #         children.pop(index)
        #     if len(children) == 1:
        #         print("Ambiguous Branch Resolved!!")
        #         node = children[0]

keywords = {'int'}