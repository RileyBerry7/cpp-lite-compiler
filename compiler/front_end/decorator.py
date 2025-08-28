from compiler.front_end.ast_node import *
from compiler.context import CompilerContext

class Decorator:
    def __init__(self, root_node: ASTNode, context: CompilerContext):
        self.root    = root_node
        self.context = context

    def mutate(self) -> None:
        """ Mutates tree in-place. """

        # Traverse List
        self._transform_dfs(self.root)

        return self.root


    def translation_unit(self, node:ASTNode, children:list[ASTNode]):
        node.name = "TRANSLATION_UNIT: FOUND"
        return node

    def _transform_dfs(self, node: ASTNode):

        # Recursive Walk
        for child in node.children:
           self._transform_dfs(child)

        # Apply Transform on Deepest Nodes
        if hasattr(self, node.name) and callable(self.__getattribute__(node.name)):
            method = self.__getattribute__(node.name)
            node = method(node, node.children)


########################################################################################################################
class ASTtoDAST(Decorator):
    """
    A class that will decorate the AST with LLVM IR relevant semantic information. The decoration process will
    recursively travers the AST and fully create a decorated version of it using the DecNode class instead of
    the lark tree class.
    """
    def __init__(self, root:ASTNode, context:CompilerContext):
        super().__init__(root_node=root, context=context)

        pass
        # self.error_table = []
        # self.symbol_table = SymbolTable
        # self.ast = ast

        # self.ast.dfs(self.visit)

        # Begin Semantic Analysis
        # self.decorate()


    # def visit(self):
    #     # DFS   Walk
    #     curr_node = ASTNode()
    #     print("Visit was called")
    #
    #     method = self.__getattribute__(curr_node.name)
    #     if method:
    #         method(curr_node)


    # def translation_unit(self, node:ASTNode):
    #     print("############################################################################################")
    #     print("Found: translation_unit")

    ####################################################################################################################
    # def decorate(self):


        # Semantic Analysis Passes

        # self.symbol_collection()  # Push symbol declarations to table
        # Errors:
        #       - Redeclaration in the same scope
        #       - Invalid storage/qualifier combinations (e.g., extern inside a block where not allowed).
        #       - Conflicting forward declarations (two structs with same name but different bases).
        #       - Ill-formed declarations (missing type, bad syntax).

        # self.symbol_binding()     # On symbol use back_track scope stack to find Def
        # Errors:
        #           - Use without def
        #           - Ambiguous reference (multiple candidates in scope).
        #           - Invalid Scope Access (using a private identifier)
        #           - Illegal Shadowing
        #

        # self.bind_symbols()

    ####################################################################################################################
    # SEMANTIC ANALYSIS PASSES

    # def bind_symbols(self):
    #     """
    #     Goal: Resolve every identifier to a symbol in the symbol table.
    #     """
        # scope_stack    = ScopeStack()
        unique_id      = 0 # Unique ID for symbols

        # Called in DFS
        # def maintain_scope(node:ASTNode):
        #     nonlocal unique_id

#             # Resolve Declaration
#             if isinstance(node, NormalDeclaration):
#
#                 # Build Symbol
#                 if node.func_body:
#                     print()
#
#                 else:
#                     pass
#                     # found_symbols = declarator_to_symbol(scope_stack.py.curr_scope, node, unique_id)
#                     # unique_id += len(found_symbols)
#
#
#                 # Check if Symbol Name Exists In Scope
#
#                 # Check if Duplicate Shares Namespace
#
#                 # ERROR: Redefined Symbol
#
#             # Resolve Use
#
#             # Create New Scope
#             elif isinstance(node, Symbol):
#                 print()
#
#
#
#         # Traverse AST
#         self.ast.dfs(maintain_scope)
#
#
#
#
#
#     ####################################################################################################################
#
# # END: class ASTtoDAST:
# ########################################################################################################################