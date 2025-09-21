# # compiler/front_end/secondary_transform.py
#
# from compiler.front_end.decorator import Decorator
# from compiler.front_end import abstract_nodes
# from compiler.front_end.abstract_nodes import ASTNode
#
# class SecondaryTransform(Decorator):
#
#     # ####################################################################################################################
#     # type_specifier:
#     def type_specifier_seq(self, node: ASTNode, children: list[ASTNode]):
#         node.name = "FUCK"
#
#     # ####################################################################################################################
#     # type_specifier:
#     # def type_specifier(self, node: ASTNode, children: list[ASTNode]):
#     #     for child in children:
#     #         if isinstance(child, abstract_nodes.Keyword):
#     #             node.name child