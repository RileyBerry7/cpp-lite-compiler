import sys
from multiprocessing.managers import Token

from lark import Tree
from compiler.front_end.symbol_table import SymbolTable, Symbol
from compiler.utils.enum_types import *
from compiler.front_end.ast_node import *


########################################################################################################################
class ASTtoDAST:
    """
    A class that will decorate the AST with LLVM IR relevant semantic information. The decoration process will
    recursively travers the AST and fully create a decorated version of it using the DecNode class instead of
    the lark tree class.
    """
    def __init__(self, ast: ASTNode):
        self.error_table = []
        self.symbol_table = SymbolTable
        self.ast = ast

        # Begin Semantic Analysis
        self.decorate()

    ####################################################################################################################
    def decorate(self):

        # Semantic Analysis Passes
        self.bind_symbols()

    ####################################################################################################################
    # SEMANTIC ANALYSIS PASSES

    def bind_symbols(self):
        """
        Goal: Resolve every identifier to a symbol in the symbol table.
        """
        scope_stack    = ScopeStack()
        unique_id      = 0 # Unique ID for symbols

        # Called in DFS
        def maintain_scope(node:ASTNode):
            nonlocal unique_id

            # Resolve Declaration
            if isinstance(node, NormalDeclaration):

                # Build Symbol
                if node.func_body:

                else:
                    decl_list = node.decl_list
                    for declarator in node.decl_list:

                        symbol = declarator_to_symbol(decl_list, declarator)


                # Check if Symbol Name Exists In Scope

                    # Check if Duplicate Shares Namespace

                        # ERROR: Redefined Symbol

            # Resolve Use

            # Create New Scope
            elif isinstance(node, Symbol):



        # Traverse AST
        self.ast.dfs(maintain_scope)





    ####################################################################################################################

# END: class ASTtoDAST:
########################################################################################################################