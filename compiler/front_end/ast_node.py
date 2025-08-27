# ast_node.py

from __future__ import annotations
from enum import Enum, auto
from typing import Union, Self, Generic, TypeVar
from compiler.utils.literal_kind import *
from compiler.utils.enum_types import *
from compiler.utils.valid_sets import FundamentalTypes
from compiler.utils.colors import colors

# ASTNode Type Template (Dynamic Typing)
NodeT = TypeVar("NodeT", bound="ASTNode")

########################################################################################################################
class ASTNode:
    """ Represents a node in the Abstract Syntax Tree (AST)."""

    def __init__(self, node_name=None, children:list[ASTNode] | None=None):

        # Abstract Node Details
        self.name = node_name
        self.children = children or []

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
    def dfs(self, visit):

        visit(self) # Call Visit Function

        # Recursively Walk Children
        for child in self.children:
            child.dfs(visit)


########################################################################################################################
#  Inheritor Nodes:  #
######################


########################################################################################################################
# TRANSLATION UNIT

class TranslationUnit(ASTNode):
    def __init__(self, declaration_list:list[ASTNode] | None = None):
        super().__init__(node_name=colors.blue.bold.underline("translation_unit"))
        self.declarations = declaration_list or []  # List of declarations (NormalDeclaration, FunctionDefinition...)

        # Add Children
        for decl in self.declarations:
            self.children.append(decl)

########################################################################################################################
# SIMPLE TYPE

class SimpleType(ASTNode):
    def __init__(self,
                 base_type:FundamentalTypes,
                 size:int,
                 signed:bool=True):

        super().__init__(node_name=colors.green("simple_type"))
        self.type_name   = base_type    # str:  base_type name
        self.size        = size         # int:  # of bits
        self.signed      = signed       # Bool: can represent negatives

        # Add Children for Pretty Printing
        self.init_children()

    def init_children(self):
        self.children.append(ASTNode(colors.teal(self.type_name.name.lower())))
        self.children.append(ASTNode(colors.teal(str(self.size))))
        self.children.append(ASTNode(colors.teal("is signed" if self.signed
                                                 else "not signed")))

########################################################################################################################
# ELABORATE TYPE

class ElaborateType(ASTNode):
    def __init__(self,
                 elaborate_kind: ElaboratedTypeKind,
                 elaborate_name: str,
                 elaborate_body: EnumBody | ClassBody | None=None,
                 enum_base     : SimpleType           | None=None,
                 is_scoped     : bool                 | None=None):

        super().__init__(node_name=colors.green("elaborate_type"))
        self.kind            = elaborate_kind #
        self.identifier      = elaborate_name #
        self.body            = elaborate_body # Optional: Defining Body

        # ENUM EXCLUSIVE ATTRIBUTES
        self.underlying_type = enum_base      # Optional: Enum base type
        self.is_scoped       = is_scoped      # Optional: Enum is_scoped

        self.init_children()

    def init_children(self):
        self.children.append(ASTNode(colors.teal(self.kind.name.lower())))
        self.children.append(ASTNode(colors.teal(self.identifier)))
        self.children.append(self.body)

########################################################################################################################
# DECLARATION SPECIFIER LIST

class DeclSpec(ASTNode):
    def __init__(self,
                 type_node: Union[SimpleType, ElaborateType],  # int, float... | class, enum
                 qualifiers:          list[str] | None =None,  # const, volatile...
                 storage_class:       str              =None,  # static, extern, thread_local...
                 function_specifiers: list[str] | None =None): # inline, constexpr, consteval, virtual, explicit...

        super().__init__(node_name="\033[38;5;28mdecl_specs\033[0m")
        self.type_node          = type_node                                            # Required: Type()
        self.qualifier_set      = set(qualifiers) if qualifiers is not None else set() # Optional: set(str)
        self.storage_class      = storage_class                                        # Optional: str
        self.func_specifier_set = set(function_specifiers) if function_specifiers is not None else set() # Optional: set(str)

        # Declaration-Level Misc. Specifiers
        self.is_constexpr:   bool = False
        self.is_consteval:   bool = False
        self.is_constinit:   bool = False
        self.is_typedef:     bool = False
        self.is_using_alias: bool = False
        self.is_friend:      bool = False
        # self.alignas_value        = None
        # self.attributes: list[str] | None = None

        # Add Children For Pretty Printing
        self.children.append(type_node)
        for child in qualifiers:
            self.children.append(ASTNode(child))
        if storage_class:
            self.children.append(ASTNode(storage_class))
        for child in function_specifiers:
            self.children.append(ASTNode(ASTNode(child)))

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
    def __init__(self,
                 decl_specs:DeclSpec,
                 declarator_list:list[NormalDeclarator] | None = None,
                 body: "CompoundBody" =None,
                 decl_kind:str="declaration"):

        super().__init__(node_name=f"\x1b[38;2;93;174;255m{decl_kind}\x1b[0m")

        # Normal declarations
        self.decl_kind   = decl_kind
        self.decl_specs  = decl_specs
        self.decl_list   = declarator_list

        # Body
        self.func_body   = body      # Used by Function / Class / Struct / Enum Definitions

        # Semantic Information
        self.symbol = None # Set during Scope Binding Pass

        self.init_children()

    def init_children(self):
        if self.decl_specs:# Add Children For Pretty Printing
            self.children.append(self.decl_specs)
        if len(self.decl_list) == 1:
            self.children.append(self.decl_list[0])
        elif len(self.decl_list) > 1:
            self.children.append(ASTNode("declarator_list", self.decl_list))
        if self.func_body:
            self.children.append(self.func_body)

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
        super().__init__(node_name=f"\x1b[38;2;255;179;71m{expr_type}\x1b[0m")  # default: orange

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
        self.children.append(ASTNode(colors.yellow(operator)))
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
        super().__init__(node_name=f"\x1b[38;2;255;107;107m{statement_type}\x1b[0m")
        # Default: red

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
        super().__init__(statement_type=colors.red("if_statement"))

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

        super().__init__(statement_type=f"\x1b[38;2;255;76;76mreturn_statement\x1b[0m")
        # Control-Flow: Saturated Red

        self.return_value = return_value  # Optional - [Expr] - usually a LiteralExpr or IdentifierExpr

        # Add Children For Pretty Printing
        if return_value:
            self.children.append(return_value)

class DeclarationStatement(Statement):
    def __init__(self, declaration:NormalDeclaration):

        super().__init__(statement_type=colors.pink("declaration_statement"))
        # Declaration Statement: red

        self.declaration = declaration  # NormalDeclaration - wrapped in a Statement

        # Add Children For Pretty Printing
        if isinstance(self.declaration, NormalDeclaration):
            self.children.append(declaration)
########################################################################################################################
# BODY NODES

class Body(ASTNode, Generic[NodeT]):
    # Generic Parameter: Member Type Template
    def __init__(self, body_type:str="body", members:list[NodeT] | None=None):
        super().__init__(node_name=colors.purple(body_type))

        self.member_list = members or []  # List of ASTNodes, may be empty

        self.init_children()

    def add_member(self, member:NodeT):
        self.member_list.append(member) # Update Member_List
        self.children.append(member)    # Update Children

    # Adds Members as Children for Pretty Printing
    def init_children(self):
        for member in self.member_list:
            self.children.append(member)

# COMPOUND BODY: Function/ If / While
class CompoundBody(Body[Statement]):
    def __init__(self, stmt_list:list[Statement] | None = None):
        super().__init__(body_type="compound_body", members=stmt_list)
        # member_list: list[Statement]

# CLASS BODY: Class / Struct / Union
class ClassBody(Body[Union[NormalDeclaration, "AccessSpecifier"]]):
    def __init__(self):
        super().__init__(body_type="class_body")

# ENUM BODY: Enum (Scoped or Unscoped)
class EnumBody(Body["Enumerator"]):
    def __init__(self, scoped:bool=False):
        super().__init__(body_type="enum_body")

class Enumerator(ASTNode):
    def __init__(self, identifier_name: str, initial_expr: ConstantExpr | None=None):
        super().__init__(node_name=colors.pink("self.identifier"))
        self.identifier   = identifier_name
        self.initial_expr = initial_expr

class AccessSpecifier(ASTNode):
    def __init__(self, access_type:AccessType):
        super().__init__(node_name="access_specifier")
        self.type = access_type

########################################################################################################################
# ERRORS

class Error(ASTNode):
    def __init__(self, error_type):
        super().__init__(node_name=colors.white.italic("ERROR: " + error_type))

        self.message = ""