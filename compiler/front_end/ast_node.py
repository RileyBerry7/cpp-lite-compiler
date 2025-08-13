# ast_node.py

from enum import Enum, auto
from typing import Union, Self
from compiler.utils.literal_kind import *

########################################################################################################################
class ASTNode:
    """ Represents a node in the Abstract Syntax Tree (AST)."""

    def __init__(self, node_name=None, children=None):

        # Abstract Node Details
        self.name = node_name
        self.children = children if children is not None else []
        self.span       = None
        # self.token_type = None

    ####################################################################################################################
    def pretty(self):
        """ Returns a string visualizing the subtree rooted at this node."""

        text_tree  = self.name + "\n"
        text_tree += self.walk(self, 1)

        return text_tree

    def walk(self, node, curr_indent):
        text_tree = ""

        if node.children:
            for child in node.children:
                text_tree += curr_indent*"  " + child.name + "\n"
                text_tree += self.walk(child, curr_indent+1)
        # else:
            # text_tree = (curr_indent+1)*"  " + "[No children]\n"

        return text_tree


########################################################################################################################
#  Inheritor Nodes:  #
######################


########################################################################################################################
# TYPE

class Type(ASTNode):
    def __init__(self, full_type:str, base_type:str, size:int, signed:bool=True, elaboration:[str]=None):
        super().__init__(node_name=full_type)
        self.type_name  = base_type
        self.size       = size
        self.signed     = signed
        self.elaboration = elaboration  # Struct, Class, Enum or None

        self.children.append(ASTNode("size: " + str(self.size) + "-bits"))

########################################################################################################################
# DECLARATION SPECIFIER LIST

class DeclSpec(ASTNode):
    def __init__(self,
                 type_node:Type      =None,
                 qualifier           =None,
                 storage_class       =None,
                 function_specifier  =None ):
        super().__init__(node_name="\033[38;5;28mdecl_specs\033[0m")
        self.type_node       = type_node           # Required
        self.qualifier       = qualifier           # Optional
        self.storage_class   = storage_class       # Optional
        self.func_specifiers = function_specifier # Optional

        self.children = [type_node]

########################################################################################################################
# POINTER LEVEL

class PtrLevel(ASTNode):
    def __init__(self,
                 scope_qualifiers: list[str] | None = None ,
                 type_qualifiers : list[str] | None = None ):

        super().__init__(node_name="PtrLevel")
        self.scope_qualifier_path = scope_qualifiers or []
        self.type_qualifier_list  = type_qualifiers  or []

########################################################################################################################
# INITIALIZER

InitElem = Union["Initializer", "Expr"]

class Initializer(ASTNode):
    def __init__(self, elements: list[InitElem] | None = None):
        super().__init__(node_name="initializer")
        self.init_list = elements or []

    def is_scalar(self) -> bool:
        return len(self.init_list) == 1 and not isinstance(self.init_list[0], Initializer)

########################################################################################################################
# NORMALIZED DECLARATOR

SuffixElem = Union["FuncSuffix", "ArraySuffix"]

class NormalDeclarator(ASTNode):
    def __init__(self,
                 ptr_chain:list[PtrLevel] | None = None,
                 reference_type=None,
                 identifier:str=None,
                 suffix_list:list[SuffixElem] | None = None):

        super().__init__(node_name="normal_declarator")

        self.ptr_chain = ptr_chain or []
        self.reference = reference_type
        self.decl_name = identifier
        self.suffixes  = suffix_list or []

    def synthesize_from_child(self, child:Self):

        # Extend Current Lists
        self.ptr_chain.extend(child.ptr_chain)
        self.suffixes.extend(child.suffixes)

        # Try To: Add Reference
        if child.reference:
            if self.reference:
                raise ValueError("Cannot have multiple reference types in a NormalDeclarator")
            else:
                self.reference = child.reference

        # Try To: Add Declaration Name
        if child.decl_name:
            if self.decl_name:
                raise ValueError("Cannot have multiple declaration names in a NormalDeclarator")
            else:
                self.decl_name = child.decl_name



########################################################################################################################
# NORMALIZED DECLARATION

class NormalDeclaration(ASTNode):
    def __init__(self, decl_specs:DeclSpec, normal_declarator:NormalDeclarator, init:Initializer):
        super().__init__(node_name="normal_declaration")
        self.decl_specs  = decl_specs
        self.decl_normal = normal_declarator
        self.decl_init   = init

########################################################################################################################
# PARAMETER

class Parameter(ASTNode):
    def __init__(self, normalized_declaration:NormalDeclaration, default_arg:Initializer=None):
        super().__init__(node_name="parameter")
        # Normalized Parameter Attributes
        self.param_declaration = normalized_declaration
        self.default_argument = default_arg             # (Optional)
                                                        # default_arg: EQUAL initializer
                                                        # initializer = list[Expr | Initializer]

########################################################################################################################
# ARRAY SUFFIX

class BaseSuffix(ASTNode):
    def __init__(self, suffix_type:str="base_suffix"):
        super().__init__(node_name=suffix_type)

class ArraySuffix(BaseSuffix):
    def __init__(self, fixed_size:"ConstantExpr"=None):
        super().__init__(suffix_type="array_suffix")
        self.size = fixed_size

class FuncSuffix(BaseSuffix):
    def __init__(self, parameter_list:list[Parameter] | None = None):
        super().__init__(suffix_type="func_suffix")
        self.param_list = parameter_list or []

########################################################################################################################
# FUNCTION SUFFIX

########################################################################################################################
# EXPRESSIONS

class ValueCategory(Enum):
    LVALUE  = auto()   # 'Locator Value' - location in memory
    PRVALUE = auto()   # 'Pure   RValue' - temporary value (RHS of an assignment)

# BASE EXPRESSION
class Expr(ASTNode):
    def __init__(self, expr_type:str="Expr"):
        super().__init__(node_name=expr_type)
        self.expr_type = expr_type
        self.value_cat = None      # Assigned at semantic analysis / decoration


class ConstantExpr(Expr):
    """ MUST BE CONSTANT - will be checked at semantic analysis """
    def __init__(self, expression:Expr):
        super().__init__(expr_type="constant_expr")
        self.expr = expression

########################################################################################################################
# PRIMITIVE EXPRESSIONS

literals = Union[str, int, float]

class LiteralExpr(Expr):
    def __init__(self, literal_type:LiteralKind, literal_value:literals=None):
        super().__init__(expr_type="literal_expr")
        self.type  = literal_type
        self.value = literal_value  # Primitive value (int, float, char, string)

class IdentifierExpr(Expr):
    def __init__(self, identifier_name:str=None):
        super().__init__(expr_type="identifier_expr")
        self.id_name = identifier_name

class UnaryExpr(Expr):
    def __init__(self, operand:Expr, operator:str=None):
        super().__init__(expr_type="unary_expr")
        self.operand  = operand
        self.operator = operator


class BinaryExpr(Expr):
    def __init__(self, left:Expr, right:Expr, operator:str=None):
        super().__init__(expr_type="binary_expr")
        self.left_operand  = left
        self.right_operand = right
        self.operator      = operator   # "+", "-", "*", "/" ...


# Assignment Expressions
class AssignExpr(Expr):
    def __init__(self, left:Expr, right:Expr, operator:str=None):
        super().__init__(expr_type="assign_expr")
        self.left_operand  = left
        self.right_operand = right
        self.operator      = operator   # "=", "+=", "-=", "*=", "/=" ...

# Comparison Expressions - (relational, equality)
class ComparisonExpr(Expr):
    def __init__(self, left:Expr, right:Expr, operator:str=None):
        super().__init__(expr_type="comparison_expr")
        self.left_operand = left
        self.right_operand = right
        self.operator = operator  # "<", ">=", "==", "!=" ...

class LogicExpr(Expr):
    def __init__(self, left:Expr, right:Expr, operator:str=None):
        super().__init__(expr_type="logic_expr")
        self.left_operand = left
        self.right_operand = right
        self.operator = operator  # "||", "&&"

# Postfix Expressions

########################################################################################################################

# class DeclName(ASTNode):
#     def __init__(self, identifier:str=None):
#         super().__init__(node_name="decl_name")
#         self.decl_name = identifier  # Identifier node

########################################################################################################################
# ERRORS

class Error(ASTNode):
    def __init__(self, error_type):
        super().__init__(node_name="\033[1;31mERROR: " + error_type +"\033[0m")

        self.message = ""

# class func_def(node):
# class type_specifier(node):
# class param_list(node):
# class param(node):
# class stmt(node):
# class expr(node):
#
# class assign_stmt(stmt):
# class return_stmt(stmt):
#
#
# class literal_expr(expr):
# class id_expr(expr):
# class bin_expr(expr):
# class un_expr(expr):