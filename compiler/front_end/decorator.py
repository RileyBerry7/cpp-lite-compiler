# decorator.py

from compiler.front_end.ast_node import *
from compiler.context import CompilerContext

########################################################################################################################

class Decorator:
    def __init__(self, root_node: ASTNode, context: CompilerContext, traversal_order:str="post"):

        """ General parent class which mimics Lark transform class.
            Use: any class methods that shadow the names of AST-nodes
                 will be transformed when object calls .walk().
        """
        self.root    = root_node # AST Root
        self.context = context   # ErrorTable, SymbolTable, ScopeStack
        self.order   = traversal_order

    def walk(self) -> None:
        """ Initiates recursive walk. """

        # Traverse List
        self._dfs(self.root)

    def _dfs(self, node: ASTNode):
        """Traverse the AST with optional pre- or post-order mutation."""

        method = getattr(self, node.name, None)

        # Pre-order
        if self.order == "pre" and callable(method):
            method(node, node.children)

        # Recursive walk
        for child in node.children:
            self._dfs(child)

        # Post-order
        if self.order == "post" and callable(method):
            method(node, node.children)

##########################################################################################

from compiler.front_end.semantic_analysis import *

class ASTtoDAST:
    def __init__(self, ast_root: ASTNode, context: CompilerContext):
        """ Decoration manager class which sequentially performs decoration/semantic-analysis passes. """

        self.root    = ast_root  # AST Root
        self.context = context   # ErrorTable, SymbolTable, ScopeStack

        # Initiate Decoration
        self.decorate()

    def decorate(self):
        pass_1 = SymbolCollector(self.root, self.context)
        pass_1.walk()
##########################################################################################
