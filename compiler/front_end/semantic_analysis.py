# semantic analysis

from compiler.front_end.ast_node import *
from compiler.context import CompilerContext
from compiler.front_end.decorator import Decorator

########################################################################################################################

########################################################################################################################
class SymbolCollector(Decorator):
    """
    Symbol-collection pass.
    """
    def __init__(self, root:ASTNode, context:CompilerContext):
        super().__init__(root_node=root, context=context, traversal_order="pre")
        # Pass-specific Attributes:
        pass

    # Node Transformation Methods
    def translation_unit(self, node: ASTNode, children: list[ASTNode]):
        node.name = "TRANSLATION_UNIT: FOUND"
########################################################################################################################

