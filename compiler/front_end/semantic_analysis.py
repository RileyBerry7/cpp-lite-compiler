# semantic analysis

from compiler.front_end.ast_node import *
from compiler.context import CompilerContext
from compiler.front_end.decorator import Decorator
from compiler.utils.enum_types import ScopeKind

########################################################################################################################
class SymbolCollector(Decorator):
    """
    Symbol-collection pass.
    """
    def __init__(self, root:ASTNode, context:CompilerContext):
        super().__init__(root_node=root, context=context, traversal_order="both")
        # Pass-specific Attributes:
        self.stack = self.context.scope_stack # alias

    ########################################################################################################################

    ########################################################################################################################
    def translation_unit_pre(self, node: ASTNode, children: list[ASTNode]):
        self.stack.enter_scope(ScopeKind.GLOBAL)

    def translation_unit_post(self, node: ASTNode, children: list[ASTNode]):

        # Exit Scope
        self.stack.exit_scope()

    # def normal_declaration(self, node: ASTNode, children: list[ASTNode]):
    #     pass
########################################################################################################################

    def enum_body_pre(self, node: ASTNode, children: list[ASTNode]):
       self.stack.enter_scope(ScopeKind.ENUM)

    def enum_body_post(self, node: ASTNode, children: list[ASTNode]):
       self.stack.exit_scope()