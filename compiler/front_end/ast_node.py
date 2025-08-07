# ast_node.py

from enum import Enum

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
# Inheritor Nodes

class Parameter(ASTNode):
    def __init__(self, param_type, param_name):
        super().__init__(node_name="parameter")
        self.param_type = param_type
        self.param_name = param_name

########################################################################################################################
class DeclSpec(ASTNode):
    def __init__(self,
                 base_type           =None,
                 type_modifier       =None,
                 qualifier           =None,
                 storage_class       =None,
                 function_specifiers =None ):

        super().__init__(node_name="decl_specs")
        self.base_type       = base_type           # Required
        self.type_modifier   = type_modifier       # Optional
        self.qualifier       = qualifier           # Optional
        self.storage_class   = storage_class       # Optional
        self.func_specifiers = function_specifiers # Optional
########################################################################################################################
class ReferenceType(str, Enum):
    REFERENCE = "&"
    DOUBLE_REFERENCE = "&&"
    DEREFERENCE = "&" "*"

class PointerChain(ASTNode):
    def __init__(self, character: ReferenceType, qualifiers=None):
        super().__init__("pointer_chain") # think something like: "int * * const & *function_name();"
        qualifiers = qualifiers if qualifiers is not None else []
        self.pointer_chain = [(character, qualifiers)]

    def append_chain(self, child_chain):
        self.pointer_chain.append(child_chain)

########################################################################################################################
# class parameter_list(ASTNode):
#     def __init__(self, children=None, params=None):
#         super().__init__(node_name="parameter_list", children=)
#         self.param_list = []

########################################################################################################################
# ERRORS

class Error(ASTNode):
    def __init__(self, error_type):
        super().__init__(node_name="ERROR: " + error_type)
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