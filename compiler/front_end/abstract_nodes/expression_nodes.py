from compiler.front_end.abstract_nodes.ast_node import ASTNode
from compiler.front_end.abstract_nodes.base_node import Expr

from enum import Enum, auto
from typing import Union
from compiler.utils.enum_types import LiteralKind
from compiler.utils.colors import colors

########################################################################################################################
# EXPRESSIONS

class ValueCategory(Enum):
    LVALUE  = auto()   # 'Locator Value' - location in memory
    PRVALUE = auto()   # 'Pure   RValue' - temporary value (RHS of an assignment)

# BASE EXPRESSION


class ConstantExpr(Expr):
    """ MUST BE CONSTANT - will be checked at semantic analysis """
    def __init__(self, expression: Expr):
        super().__init__(expr_type="constant_expr")
        self.expr = expression

########################################################################################################################
# PRIMITIVE EXPRESSIONS

literals = Union[str, int, float]

class LiteralExpr(Expr):
    def __init__(self, literal_type:LiteralKind, literal_value:literals=None):
        super().__init__(expr_type=colors.gold("literal_expr"))  # Literal values

        self.type  = literal_type
        self.value = literal_value  # Primitive value (int, float, char, string)

symbol: "Symbol | None" = None

class IdentifierExpr(Expr):
    def __init__(self, identifier_name:str=None):
        super().__init__(expr_type="identifier_expr")
        self.id_name = identifier_name

        # Semantic Information
        self.symbol = None # Set during Scope Binding Pass

class UnaryExpr(Expr):
    def __init__(self, operand: Expr, operator:str=None):
        super().__init__(expr_type="unary_expr")
        self.operand  = operand
        self.operator = operator


class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator:str=None):
        super().__init__(expr_type="binary_expr")
        self.left_operand  = left
        self.right_operand = right
        self.operator      = operator   # "+", "-", "*", "/" ...

        # Add Children For Pretty Printing
        self.children.append(left)
        self.children.append(ASTNode(colors.yellow(operator)))
        self.children.append(right)


# Assignment Expressions
class AssignExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator:str=None):
        super().__init__(expr_type="assign_expr")
        self.left_operand  = left
        self.right_operand = right
        self.operator      = operator   # "=", "+=", "-=", "*=", "/=" ...

# Comparison Expressions - (relational, equality)
class ComparisonExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator:str=None):
        super().__init__(expr_type="comparison_expr")
        self.left_operand = left
        self.right_operand = right
        self.operator = operator  # "<", ">=", "==", "!=" ...

        # Add Children For Pretty Printing
        self.children.append(left)
        self.children.append(ASTNode(operator))
        self.children.append(right)

class LogicExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator:str=None):
        super().__init__(expr_type="logic_expr")
        self.left_operand = left
        self.right_operand = right
        self.operator = operator  # "||", "&&"

# Postfix Expressions
########################################################################################################################
#