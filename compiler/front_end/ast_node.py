# ast_node.py

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

    # def IDENTIFIER(self, token):
    #     return str(token)  # or just token.value

# class external_declaration(ASTNode):
#     def __init__(self, node_name="external_declaration"):
#         super().__init__(node_name=node_name)

########################################################################################################################

class parameter(ASTNode):
    def __init__(self, param_type, param_name):
        super().__init__(node_name="parameter")
        self.param_type = param_type
        self.param_name = param_name
########################################################################################################################
# class parameter_list(ASTNode):
#     def __init__(self, children=None, params=None):
#         super().__init__(node_name="parameter_list", children=)
#         self.param_list = []

########################################################################################################################


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