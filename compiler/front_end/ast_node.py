# ast_node.py

from enum import Enum
from typing import Union, Self

########################################################################################################################
class ASTNode:
    """ Represents a node in the Abstract Syntax Tree (AST)."""

    def __init__(self, node_name=None, children=None):

        # Abstract Node Details
        self.name = node_name
        self.children = children if children is not None else []

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

        self.ptr_chain.extend(child.ptr_chain)
        self.reference = child.reference
        self.decl_name = child.decl_name
        self.suffixes.extend(child.suffixes)




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
    def __init__(self, normalized_declaration:NormalDeclaration):
        super().__init__(node_name="parameter")
        # Normalized Parameter Attributes
        self.param_declaration = normalized_declaration

########################################################################################################################
# EXPRESSIONS

class Expr(ASTNode):
    def __init__(self, expr_type:str="Expr"):
        super().__init__(node_name=expr_type)
        self.type  = None # Filled in semantic analysis
        self.value = None # Constant Value if any

class PrimaryExpr(Expr):
    def __init__(self, identifier:str=None, literal:str=None):
        super().__init__(expr_type="primary_expr")
        self.identifier = identifier
        self.literal   = literal

# class UnaryExpr(Expr):
#
# class BinaryExpr(Expr):
#
# # Semantic structure
# class AssignExpr(Expr):
#
# class CondExpr(Expr):
#
# class RelExpr(Expr):

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