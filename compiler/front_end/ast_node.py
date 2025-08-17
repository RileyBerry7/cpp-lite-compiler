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
# TRANSLATION UNIT

class TranslationUnit(ASTNode):
    def __init__(self, declaration_list:list[ASTNode] | None = None):
        super().__init__(node_name="\033[1;38;5;226mtranslation_unit\033[0m")
        self.declarations = declaration_list or []  # List of declarations (NormalDeclaration, FunctionDefinition...)

        # Add Children
        for decl in self.declarations:
            self.children.append(decl)

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
        self.func_specifiers = function_specifier  # Optional

        # Add Children For Pretty Printing
        self.children.append(type_node)
        if qualifier:
            self.children.append(ASTNode(qualifier))
        if storage_class:
            self.children.append(ASTNode(storage_class))
        if function_specifier:
            self.children.append(ASTNode(function_specifier))

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
                 suffix_list:list[SuffixElem] | None = None,
                 initializer:Initializer | None = None):

        super().__init__(node_name="\033[38;5;28mnormal_declarator\033[0m")

        self.ptr_chain   = ptr_chain or []
        self.reference   = reference_type
        self.decl_name   = identifier
        self.suffixes    = suffix_list or []
        self.initializer = initializer  # Optional

        # Add Children For Pretty Printing
    #     self.init_children()
    #
    # def init_children(self):
        # if self.ptr_chain:
        #     self.children.append(ASTNode("ptr_chain", self.ptr_chain))
        # if self.reference:
        #     self.children.append(ASTNode(self.reference))
        # if self.decl_name:
        #     self.children.append(ASTNode(self.decl_name))
        # if self.suffixes:
        #     self.children.append(ASTNode("suffix_list", self.suffixes))
        # if  self.initializer:
        #     self.children.append( self.initializer)


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

        # Reinitialize Children Every Merge
        # self.init_children()


#

########################################################################################################################
# NORMALIZED DECLARATION

class NormalDeclaration(ASTNode):
    def __init__(self, decl_specs:DeclSpec, declarator_list:list[NormalDeclarator] | None = None, func_body:"CompoundStatement"=None):
        super().__init__(node_name="\x1b[1;91mnormal_declaration\x1b[0m")
        self.decl_specs  = decl_specs
        self.decl_list   = declarator_list
        self.func_body   = func_body # Only used by Function Definitions

        # Semantic Information
        self.symbol = None # Set during Scope Binding Pass

        # Add Children For Pretty Printing
        if decl_specs:
            self.children.append(decl_specs)
        if len(declarator_list) == 1:
            self.children.append(declarator_list[0])
        elif len(declarator_list) > 1:
            self.children.append(ASTNode("declarator_list"), declarator_list)
        if func_body:
            self.children.append(func_body)

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
        super().__init__(node_name=f"\x1b[1;38;5;226m{expr_type}\x1b[0m")
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

symbol: "Symbol | None" = None

class IdentifierExpr(Expr):
    def __init__(self, identifier_name:str=None):
        super().__init__(expr_type="identifier_expr")
        self.id_name = identifier_name

        # Semantic Information
        self.symbol = None # Set during Scope Binding Pass

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

        # Add Children For Pretty Printing
        self.children.append(left)
        self.children.append(ASTNode(operator))
        self.children.append(right)


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

        # Add Children For Pretty Printing
        self.children.append(left)
        self.children.append(ASTNode(operator))
        self.children.append(right)

class LogicExpr(Expr):
    def __init__(self, left:Expr, right:Expr, operator:str=None):
        super().__init__(expr_type="logic_expr")
        self.left_operand = left
        self.right_operand = right
        self.operator = operator  # "||", "&&"

# Postfix Expressions
########################################################################################################################
# STATEMENTS

class Statement(ASTNode):
    def __init__(self, statement_type:str="statement"):
        super().__init__(node_name=f"\x1b[1;91m{statement_type}\x1b[0m")
        self.statement_type = statement_type
        # Metadata For Semantic Information
        # ...

# Inheritor Statements
class ExprStatement(Statement):
    def __init__(self, expression:Expr):
        super().__init__(statement_type="expr_statement")
        self.expr = expression

        # Add Children For Pretty Printing
        self.children.append(expression)

class IfStatement(Statement):
    def __init__(self, condition:Expr, then_branch:Statement, else_branch:Statement=None):
        super().__init__(statement_type="if_statement")
        self.if_condition = condition   # Required - [Expr]      - usually a ComparisonExpr
        self.then_branch = then_branch  # Required - [Statement] - usually a CompoundStatement
        self.else_branch = else_branch  # Optional - [Statement | None]

        # Add Children For Pretty Printing
        self.children.append(condition)
        self.children.append(then_branch)
        if else_branch:
            self.children.append(else_branch)

class ReturnStatement(Statement):
    def __init__(self, return_value:Expr=None):
        super().__init__(statement_type="return_statement")
        self.return_value = return_value  # Optional - [Expr] - usually a LiteralExpr or IdentifierExpr

        # Add Children For Pretty Printing
        if return_value:
            self.children.append(return_value)

class CompoundStatement(Statement):
    def __init__(self, statement_list:list[Statement] | None = None):
        super().__init__(statement_type="compound_statement")
        self.statements = statement_list or []  # List of Statements, may be empty

        # Add Children For Pretty Printing
        for stmt in self.statements:
            self.children.append(stmt)

class DeclarationStatement(Statement):
    def __init__(self, declaration:NormalDeclaration):
        super().__init__(statement_type="declaration_statement")
        self.declaration = declaration  # NormalDeclaration - wrapped in a Statement

        # Add Children For Pretty Printing
        if isinstance(self.declaration, NormalDeclaration):
            self.children.append(declaration)

########################################################################################################################
# ERRORS

class Error(ASTNode):
    def __init__(self, error_type):
        super().__init__(node_name="\033[1;31mERROR: " + error_type +"\033[0m")

        self.message = ""