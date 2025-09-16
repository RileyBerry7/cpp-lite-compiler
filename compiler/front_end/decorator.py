# decorator.py

from compiler.front_end.abstract_nodes.ast_node import *
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

        # Base Methods
        method = getattr(self, node.name, None)

        # Pre/Post Specific Methods
        pre_method = getattr(self, f"{node.name}_pre", None)
        post_method = getattr(self, f"{node.name}_post", None)

        # Fall-back to 'Default' Method
        if method is None and pre_method is None and post_method is None:
            method = getattr(self, "__default__", None)

        # Pre-order
        if self.order in ("pre", "both"):
            if callable(pre_method):
                pre_method(node, node.children)
            if callable(method):
                method(node, node.children)

        # Recursive walk
        for child in node.children:
            self._dfs(child)

        # Post-order
        if self.order in ("post", "both"):
            if callable(method):
                method(node, node.children)
            if callable(post_method):
                post_method(node, node.children)

##########################################################################################

from compiler.front_end.semantic_analysis import *

class ASTtoDAST:
    def __init__(self, ast_root: ASTNode, context: CompilerContext):
        """ Decoration manager class which sequentially performs decoration/semantic-analysis passes. """

        self.root    = ast_root  # AST Root
        self.context = context   # ErrorTable, SymbolTable, ScopeStack

        # # Initiate Decoration
        # self.decorate()

    def decorate(self):
        # pass_0 =
        pass_1 = SymbolCollector(self.root, self.context)
        pass_1.walk()

##########################################################################################
