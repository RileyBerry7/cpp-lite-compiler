from __future__ import annotations
from compiler.front_end.abstract_nodes.ast_node import ASTNode
from compiler.front_end.abstract_nodes.misc_nodes import *
from compiler.utils.colors import colors
from typing import Generic, TypeVar, Union, Self
from compiler.utils.enum_types import *
from compiler.utils.valid_sets import FundamentalTypes
from compiler.utils.valid_sets import IdentifierIntention

# ASTNode Type Template (Dynamic Typing)
NodeT = TypeVar("NodeT", bound="ASTNode")
MemberT = TypeVar("MemberT", bool, int, str, float)


class Statement(ASTNode):
    def __init__(self, statement_type: str = "statement"):
        super().__init__(node_name=statement_type)
        self.statement_type = statement_type
        self.ansi_color = colors.red

########################################################################################################################

class Body(ASTNode, Generic[NodeT]):
    # Generic Parameter: Member Type Template
    def __init__(self, body_type:str="body", members:list[NodeT] | None=None):
        super().__init__(node_name=body_type)

        self.member_list = members or []  # List of ASTNodes, may be empty
        self.ansi_color = colors.purple
        self.init_children()

    def add_member(self, member:NodeT):
        self.member_list.append(member) # Update Member_List
        self.children.append(member)    # Update Children

    # Adds Members as Children for Pretty Printing
    def init_children(self):
        for member in self.member_list:
            self.children.append(member)
########################################################################################################################



########################################################################################################################
# NORMALIZED DECLARATION

class NormalDeclaration(ASTNode):
    def __init__(self,
                 decl_specs:DeclSpec,
                 declarator_list:list["NormalDeclaration"] | None = None,
                 body: "CompoundBody" =None,
                 decl_kind:str="normal_declaration"):

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
# TRANSLATION UNIT

class TranslationUnit(ASTNode):
    def __init__(self, declaration_list: list[ASTNode] | None = None):
        super().__init__(node_name="translation_unit")


        # List of External Declarations
        self.declarations = declaration_list or []

        # Add Color for Pretty-Printing
        self.ansi_color = colors.blue.bold.underline

        # Add Children for Pretty-Printing
        for member in self.declarations:
            self.children.append(member)

########################################################################################################################
# SIMPLE TYPE

class SimpleType(ASTNode):
    def __init__(self,
                 base_type:FundamentalTypes,
                 size:int,
                 signed:bool=True):

        super().__init__(node_name="simple_type")
        self.type_name   = base_type    # str:  base_type name
        self.size        = size         # int:  # of bits
        self.signed      = signed       # Bool: can represent negatives

        # Add Color for Pretty-Printing
        self.ansi_color = colors.green

        # Add Children for Pretty-Printing
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

        super().__init__(node_name="elaborate_type")
        self.kind            = elaborate_kind #
        self.identifier      = elaborate_name #
        self.body            = elaborate_body # Optional: Defining Body

        # ENUM EXCLUSIVE ATTRIBUTES
        self.underlying_type = enum_base      # Optional: Enum base type
        self.is_scoped       = is_scoped      # Optional: Enum is_scoped

        # Add Color for Pretty-Printing
        self.ansi_color = colors.green

        # Add Children for Pretty-Printing
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

        super().__init__(node_name="decl_specs")
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

        # Add Color for Pretty-Printing
        self.ansi_color = colors.dark_green

        # Add Children For Pretty-Printing
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

        super().__init__(node_name="ptr_evel")
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

        super().__init__(node_name="normal_declarator")

        self.ptr_chain   = ptr_chain or []
        self.reference   = reference_type
        self.decl_name   = identifier
        self.suffixes    = suffix_list or []
        self.initializer = initializer  # Optional

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
# PARAMETER

class Parameter(ASTNode):
    def __init__(self, normalized_declaration:NormalDeclaration, default_arg:Initializer=None):
        super().__init__(node_name="parameter")
        # Normalized Parameter Attributes
        self.param_declaration = normalized_declaration
        self.default_argument = default_arg             # (Optional)
        # default_arg: EQUAL initializer
        # initializer = list[Expr | Initializer]

# misc_nodes.py

# STATEMENTS

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


# BODY NODES


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

# FUNCTION BODY:
# class FunctionBody(Body[])

########################################################################################################################
class Enumerator(ASTNode):
    def __init__(self, identifier_name: str, initial_expr: ConstantExpr | None=None):
        super().__init__(node_name=colors.pink("self.identifier"))
        self.identifier   = identifier_name
        self.initial_expr = initial_expr
########################################################################################################################

from compiler.utils.enum_types import AccessType
class AccessSpecifier(ASTNode):
    def __init__(self, access_type:AccessType):
        super().__init__(node_name="access_specifier")
        self.type = access_type





# v ISO C++ COMPLIANT v
########################################################################################################################
class Literal(ASTNode):
    def __init__(self, kind: LiteralKind, value):
        super().__init__(node_name=kind.lower()+"_literal: "+str(value))
        self.literal_kind  = kind
        self.literal_value = value

        # Pretty Printing
        self.ansi_color = colors.grey

########################################################################################################################
class Keyword(ASTNode):
    def __init__(self, keyword: str):
        super().__init__(node_name="keyword: " + keyword)
        self.lexeme = keyword
        self.ansi_color = colors.grey

########################################################################################################################
class Operator(ASTNode):
    def __init__(self, lexeme: str):
        super().__init__(node_name="operator: " + lexeme)
        self.op_string = lexeme
        self.ansi_color = colors.grey

########################################################################################################################
class Identifier(ASTNode):
    def __init__(self, id_name: str, intent: IdentifierIntention | None = IdentifierIntention.UNRESOLVED):
        super().__init__(node_name="identifier: " + id_name)
        self.id_name = id_name
        self.symbol_id: int | None = None
        self.ansi_color = colors.grey
        self.intention = intent

        # Pretty Printing
        self.children.append(ASTNode(self.intention.name, None, colors.grey))

    def update_intent(self, new_intent: IdentifierIntention):
        self.intention = new_intent
        self.children[0].name = new_intent.name

########################################################################################################################
# AMBIGUOUS IDENTIFIER

class AmbigIdentifer(Identifier):

    """ During semantic analysis this identifier will check for its own resolution condition. If the
        resolution condition is met, then this ambiguous branch will become the true branch, else it
        will be marked 'dead_branch' and pruned"""

    def __init__(self, identifer: Identifier):
        super().__init__(identifer.id_name, identifer.intention)
        self.name = "ambig_identifier: " + identifer.id_name
        # INTENT <- Resolution Condition

        self.ansi_color = colors.red # Pretty Printing

########################################################################################################################

class NormalizedType(ASTNode):
    def __init__(self):
        super().__init__(node_name="normalized_type")

        self.core: TypeCore | None = None                     # Represents Type's Core
        self.modifiers  : Body[Modifiers] = Body[Modifiers]() # List of Core Modifiers (Prefix, Suffix, Suffix...)

        self.attrs   = None # will implement later maybe

    # def synthesize_from_child(self, child:Self):

########################################################################################################################

class ListNode(ASTNode, Generic[MemberT]):
    """ Generic list templated with any any built-in type. """
    def __init__(self, list_name:str, members:list[MemberT] | None=None):
        super().__init__(node_name=
                         f"{list_name}_list: {', '.join(str(i) for i in members)}")

        self.member_list = members or []  # List of members, may be empty
        self.ansi_color = colors.purple

    def add_member(self, new_member:MemberT):
        self.member_list.append(new_member)
    def extend_list(self, new_list:list[MemberT] | ListNode[MemberT]):
        if isinstance(new_list, list):
            self.member_list.extend(new_list)
        elif isinstance(new_list, ListNode):
            self.member_list.extend(new_list.member_list)
########################################################################################################################
# CORE
class TypeCore(ASTNode):
    """ Abstract base for NormalizedType cores. These are all abstracted derivations of type_specifier_seq. """
    def __init__(self, node_name:str):
        super().__init__(node_name=node_name)
        pass
########################################################################################################################
# CORE_TYPES

# BuiltInType   # int;                  <- simple_type_specifier
class BuiltInType(TypeCore):
    def __init__(self,
                 base_type:FundamentalTypes,
                 size:int,
                 signed:bool=True):

        super().__init__(node_name="builtin_type")
        self.base_type   = base_type    # str:  base_type name
        self.size        = size         # int:  # of bits
        self.signed      = signed       # Bool: can represent negatives

        # Used for upwards synthesize
        # self.type_string: ListNode[str] = ListNode[str]("type_string")

        # Add Color for Pretty-Printing
        self.ansi_color = colors.green

    #     # Add Children for Pretty-Printing
    #     self.init_children()
    #
    # def init_children(self):
    #     self.children.append(ASTNode(colors.teal(self.type_name.name.lower())))
    #     self.children.append(ASTNode(colors.teal(str(self.size))))
    #     self.children.append(ASTNode(colors.teal("is signed" if self.signed
    #                                              else "not signed")))
    #



# QualifiedID   # A::B foo;             <- qualified_id <- nested_name_specifier
# TemplateID    # Box<int> Shape;       <- simple_template_id
# DeclType      # decltype(x) y;        <- decltype_specifier
# DeclTypeAuto  # decltype(auto) y = 3; <- decltype_specifier
# Auto          # auto x = 5;           <- decltype_specifier
# DependentName # typename T::iterator; <- typename_specifier

# ElaboratedType
#
########################################################################################################################
class Modifiers(ASTNode):
    pass

class Suffix(ASTNode):
    def __init__(self, suffix_type:str):
        super().__init__(node_name=suffix_type+"_suffix")
        self.ansi_color = colors.purple

########################################################################################################################
# ARRAY SUFFIX

class ArraySuffix(Suffix, Modifiers):
    def __init__(self, bound: ConstantExpr | None = None):
        super().__init__(suffix_type="array")
        self.array_bound: bound

        if bound is not None:
            self.children.append(bound)

########################################################################################################################
# FUNCTION SUFFIX

class FunctionSuffix(Suffix, Modifiers):
    def __init__(self, parameter_list:ASTNode | None = None):
        super().__init__(suffix_type="function")
        self.parameters = parameter_list
        self.cv_list    = None
        self.ansi_color = colors.green

        if parameter_list:
            self.children.append(parameter_list)

########################################################################################################################

########################################################################################################################

########################################################################################################################
# EXPRESSIONS

########################################################################################################################
# BASE EXPRESSION

class Expr(ASTNode):
    def __init__(self, expr_type:str):
        super().__init__(node_name=expr_type+"_expression")  # default: orange
        self.expr_type = expr_type
        self.ansi_color = colors.orange
########################################################################################################################


class ConstantExpr(Expr):
    """ MUST BE CONSTANT - will be checked at semantic analysis """
    def __init__(self, expression: ASTNode):
        super().__init__(expr_type="constant")
        self.expr = expression

        self.children.append(expression)

########################################################################################################################
# PRIMARY EXPRESSIONS

# class Literal():
# class Identifier():

########################################################################################################################
# UNARY

class UnaryExpr(Expr):
    def __init__(self, subject: ASTNode, operation: ASTNode):
        """ Contains:
                Postfix Expressions
                Prefix Expressions
        """
        super().__init__(expr_type="unary")
        self.subject   = subject
        self.operation = operation

        # Add Children For Pretty Printing
        subject.ansi_color = colors.yellow
        self.children.append(subject)
        self.children.append(operation)

########################################################################################################################
# CAST

class CastExpr(Expr):
    def __init__(self, cast_type: ASTNode, subject: ASTNode):
        """ Contains:
                C Style Cast   <- ambiguous_cast
                C++ Style Cast
        """
        super().__init__(expr_type="cast")
        self.cast_type = cast_type
        self.subject = subject

        # Add Children For Pretty Printing
        cast_type.ansi_color = colors.yellow
        self.children.append(cast_type)
        self.children.append(subject)

########################################################################################################################
# MEMBER ACCESS

class MemberAccess(Expr):
    def __init__(self, source: ASTNode, access_type: Operator, target: ASTNode):
        """ Contains:
                pm_expression
        """
        super().__init__(expr_type="member_access")
        self.source   = source
        self.operator = access_type
        self.target   = target

        # Add Children For Pretty Printing
        self.children.append(source)
        access_type.ansi_color = colors.yellow
        self.children.append(access_type)
        self.children.append(target)

########################################################################################################################

class BinaryExpr(Expr):
    """ Represents:
            Arithmetic Expression (multiplicative, additive)
            Comparative Expressions (relational, equality)
            Bitwise Expressions (shift, relational, equality)
    """
    def __init__(self, left: ASTNode, operator: Operator , right: ASTNode):
        super().__init__(expr_type="binary")
        self.left_operand  = left
        self.right_operand = right
        self.operator      = operator   # "+", "-", "*", "/" ...

        # Add Children For Pretty Printing
        self.children.append(left)
        operator.ansi_color = colors.yellow
        self.children.append(operator)
        self.children.append(right)

########################################################################################################################
# LOGICAL EXPRESSION

class LogicExpr(Expr):
    def __init__(self, left: ASTNode, operator: Operator , right: ASTNode):
        """ Contains:
                Logical And Expressions (&&)
                Logical Or Expressions (||)
        """
        super().__init__(expr_type="logic")
        self.left_operand = left
        self.right_operand = right
        self.operator = operator  # "+", "-", "*", "/" ...

        # Add Children For Pretty Printing
        self.children.append(left)
        operator.ansi_color = colors.yellow
        self.children.append(operator)
        self.children.append(right)

########################################################################################################################
# CONDITIONAL EXPRESSION

class ConditionalExpr(Expr):
    def __init__(self, if_cond: ASTNode, then_case: ASTNode , else_case: ASTNode):
        """ Contains:
                conditional_expressions ( if ? then : else ;)
        """
        super().__init__(expr_type="conditional")
        self.if_cond   = if_cond
        self.then_case = then_case
        self.else_case = else_case  # "+", "-", "*", "/" ...

        # Add Children For Pretty Printing
        self.children.append(if_cond)
        if_cond.ansi_color = colors.yellow
        self.children.append(if_cond)
        self.children.append(else_case)

########################################################################################################################
# Assignment Expressions
class AssignExpr(Expr):
    def __init__(self, left: ASTNode, right: ASTNode, operator: Operator):
        super().__init__(expr_type="assign")
        self.left_operand  = left
        self.right_operand = right
        self.operator      = operator   # "=", "+=", "-=", "*=", "/=" ...

        # Add Children For Pretty Printing
        self.children.append(left)
        operator.ansi_color = colors.yellow
        self.children.append(operator)
        self.children.append(right)

