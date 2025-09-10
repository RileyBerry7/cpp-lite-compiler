# transformer.py
import lark
from lark import Transformer
from compiler.front_end import abstract_nodes
from compiler.front_end.abstract_nodes import ASTNode

from compiler.utils.enum_types import *

from compiler.utils.token_to_literal_kind import *
from compiler.utils.lexeme_to_number import lexeme_to_number
from compiler.utils.resolve_simple_type import resolve_simple_type
from compiler.utils.colors import colors

########################################################################################################################
class CSTtoAST(Transformer):
    """
    A Transformer that converts a CST to an AST.
    """

    def __default__(self, data, children, meta):
        abstract_node = abstract_nodes.ast_node.ASTNode(data, children)
        return abstract_node

    def __default_token__(self, token):

        return ASTNode(token.type, [ASTNode(token.value)])

    ####################################################################################################################
    # Ambiguous Nodes
    def _ambig(self, possible_trees):
        from compiler.utils.colors import colors
        branches = []
        for path in possible_trees:
            if isinstance(path, abstract_nodes.ASTNode):
                path.ansi_color = colors.orange
                branches.append(path)
            else:
                branches.append(abstract_nodes.ASTNode("Non-abstract Path"))
                branches[-1].ansi_color = colors.red
        ambig_node = abstract_nodes.ASTNode("Ambiguity", branches)
        ambig_node.ansi_color = colors.red.underline
        return ambig_node

    # ####################################################################################################################
    # # TRANSLATION UNIT
    # def translation_unit(self, children):
    #     return abstract_nodes.TranslationUnit(children)
    #
    # def declaration_seq(self, children):
    #     for child in children:
    #         if isinstance(child, abstract_nodes.ASTNode):
    #             from compiler.utils.colors import colors
    #             child.ansi_color = colors.green
    #     return abstract_nodes.ASTNode("declaration_seq", children)
    # ####################################################################################################################
    # # EXTERNAL DECLARATION
    #
    # def external_declaration(self, children):
    #     # if children and isinstance(children[0], abstract_nodes.NormalDeclaration):
    #     #     return children[0]
    #     #
    #     # return abstract_nodes.Error("Invalid external declaration")
    #      return children[0]
    #
    #
    # ####################################################################################################################
    # def class_type(self, children):
    #
    #     kind = ElaboratedTypeKind.CLASS
    #     identifier = "ERROR: id not-found"
    #     body = None
    #
    #     # Loop through Children, Build Elaborate Type
    #     for child in children:
    #
    #         # Check if Union
    #         if child.name == "union":
    #             kind = ElaboratedTypeKind.UNION
    #
    #         # Check for Scope Qualifier
    #         elif child.name == "scope_qualifier":
    #             pass
    #
    #         # Check for Body
    #         if isinstance(child, abstract_nodes.ClassBody):
    #             body = child
    #
    #         # Else is Identifier
    #         else:
    #             identifier = child.name
    #
    #     return abstract_nodes.ElaborateType(kind, identifier, body)
    #
    # def enumerator(self, children):
    #
    #     id_name = children[0].name
    #
    #     if len(children) == 1:
    #         return abstract_nodes.Enumerator(children[0].name)
    #     elif len(children) == 3:
    #         return abstract_nodes.Enumerator(children[0].name, children[2])
    #     else:
    #         return Error("Invalid enumerator")
    #
    # ################################################################################################################
    #
    # def enum_type(self, children):
    #
    #     kind       = ElaboratedTypeKind.ENUM
    #     identifier = "ERROR: id not-found"
    #     is_scoped  = None
    #     enum_base  = resolve_simple_type(['int'])
    #     body       = None
    #
    #     # Loop through Children, Build Elaborate Type
    #     for child in children:
    #
    #         # Check if Scoped
    #         if child.name == "class" or child.name == "struct":
    #             is_scoped = True
    #
    #         # Check for Scope Qualifier
    #         elif child.name == "scope_qualifier":
    #             pass
    #
    #         # Check for Enum Base
    #         elif child.name == "enum_base":
    #             specifier_seq = []
    #             if isinstance(child.children[1], compiler.front_end.abstract_nodes.ast_node.ASTNode):
    #                 for specifier in child.children[1].children:
    #                     specifier_seq.append(specifier.name)
    #             enum_base = resolve_simple_type(specifier_seq)
    #
    #         # Check for Body
    #         if isinstance(child, abstract_nodes.EnumBody):
    #             body = child
    #
    #         # Else is Identifier
    #         else:
    #             identifier = child.name
    #
    #     return abstract_nodes.ElaborateType(kind, identifier, body, enum_base, is_scoped)
    #
    # def enumerator(self, children):
    #
    #     id_name = children[0].name
    #
    #     if len(children) == 1:
    #         return abstract_nodes.Enumerator(children[0].name)
    #     elif len(children) == 3:
    #         return abstract_nodes.Enumerator(children[0].name, children[2])
    #     else:
    #         return abstract_nodes.Error("Invalid enumerator")
    #
    #
    # ####################################################################################################################
    # def decl_specifier_seq(self, children):
    #
    #     # Initialize Empty Specs
    #     simple_type_list    = []
    #     qualifiers          = []
    #     function_specifiers = []
    #     storage_class       = None
    #     simple_type         = None
    #     elaborate_type      = None
    #
    #     # Initialize Specifier Flags
    #     is_constexpr:   bool = False
    #     is_consteval:   bool = False
    #     is_constinit:   bool = False
    #     is_typedef:     bool = False
    #     is_using_alias: bool = False
    #     is_friend:      bool = False
    #
    #     ################################################################################################################
    #
    #     # Determine Children
    #     if children:
    #         for child in children:
    #             if isinstance(child, compiler.front_end.abstract_nodes.ast_node.ASTNode):
    #
    #                 # FOUND: Simple Type Specifier
    #                 if child.name == "simple_type_specifier":
    #                     simple_type_list.append(child.children[0].name)
    #
    #                 # FOUND: Elaborate Type Specifier
    #                 elif isinstance(child, abstract_nodes.ElaborateType):
    #                     elaborate_type = child
    #
    #                 # FOUND: Type Qualifier
    #                 elif child.name == "type_qualifier":
    #                     qualifiers.append(child.children[0].name)
    #
    #                 # Found: Storage Class Specifier
    #                 elif child.name == "storage_class_specifier":
    #                     # SEMANTIC ERROR: multiple storage class specifiers
    #                     if storage_class is not None:
    #                         return abstract_nodes.Error("Multiple storage class specifiers found")
    #                     storage_class = child.children[0].name
    #
    #                 # Found: Function Specifier
    #                 elif child.name == "function_specifier":
    #                     function_specifiers.append(child.children[0].name)
    #
    #                 ####################################################################################################
    #                 # FLAG CHECKING
    #
    #                 # Found: Constexpr Flag
    #                 elif child.name == "constexpr":
    #                     is_constexpr = True
    #
    #                 # Found: Consteval Flag
    #                 elif child.name == "consteval":
    #                     is_consteval = True
    #
    #                 # Found: Constinit Flag
    #                 elif child.name == "constinit":
    #                     is_constinit = True
    #
    #                 # Found: Typedef Flag
    #                 elif child.name == "typedef":
    #                     is_typedef = True
    #
    #                 # Found: Using Flag
    #                 elif child.name == "using":
    #                     is_using_alias = True
    #
    #                 # Found: Friend Flag
    #                 elif child.name == "friend":
    #                     is_friend = True
    #
    #     # END - Determine Children
    #     ################################################################################################################
    #
    #
    #     # Resolve Simple Type
    #     if not simple_type_list:
    #         simple_type = None
    #     else:
    #         simple_type = resolve_simple_type(simple_type_list)
    #
    #     # CHECK: Mutual-Exclusivity Between Simple & Elaborate Type
    #     if elaborate_type and simple_type:
    #         return abstract_nodes.Error("'Elaborate' and 'Simple' types are mutually exclusive.")
    #
    #     elif elaborate_type:
    #         resolved_type = elaborate_type
    #
    #     elif simple_type:
    #         resolved_type = simple_type
    #
    #     else:
    #         return abstract_nodes.Error("Neither 'Elaborate' nor 'Simple' type was found.")
    #
    #     # CONSTRUCT: Declaration Specifier Node
    #     specifier_node = abstract_nodes.DeclSpec(resolved_type, qualifiers, storage_class, function_specifiers)
    #
    #     # ASSIGN: Flag Specifiers
    #     specifier_node.is_constexpr   = is_constexpr
    #     specifier_node.is_consteval   = is_consteval
    #     specifier_node.is_constinit   = is_constinit
    #     specifier_node.is_typedef     = is_typedef
    #     specifier_node.is_using_alias = is_using_alias
    #     specifier_node.is_friend      = is_friend
    #
    #     # RETURN: Declaration Specifier Node
    #     return specifier_node
    #
    # ####################################################################################################################
    # # PARAMETER
    # def parameter(self, children):
    #
    #     param_declaration = children[0]
    #     default_args = None
    #
    #
    #
    #
    #     return abstract_nodes.Parameter(param_declaration, default_args)
    #
    # def default_arg(self, children):
    #     if len(children) >= 1 and isinstance(children[1], abstract_nodes.Initializer):
    #         return children[1]
    #     else:
    #         return abstract_nodes.Error("No Initializer Found for Default Argument")
    #
    #
    # def initializer(self, children):
    #     for child in children:
    #         if isinstance(child, compiler.front_end.abstract_nodes.ast_node.ASTNode):
    #             if isinstance(child, compiler.front_end.abstract_nodes.base_node.Expr):
    #                 return abstract_nodes.Initializer(child)
    #
    #             if isinstance(child, abstract_nodes.Initializer):
    #                 return child
    #
    # ####################################################################################################################
    # # DECLARATOR
    # def declarator(self, children):
    #     normalized_declarator = abstract_nodes.NormalDeclarator()
    #     for child in children:
    #         if isinstance(child, compiler.front_end.abstract_nodes.ast_node.ASTNode) and child.name == "ptr_list":
    #             for ptr_lvl in child.children:
    #                 if isinstance(ptr_lvl, abstract_nodes.PtrLevel):
    #                     normalized_declarator.ptr_chain.append(ptr_lvl) # Might be backwards!!!
    #
    #         if isinstance(child,
    #                       compiler.front_end.abstract_nodes.ast_node.ASTNode) and child.name == "reference_operator":
    #             if children.children and child.children[0].name == "AND":
    #                 normalized_declarator.reference = "lvalue"
    #             else:
    #                 normalized_declarator.reference = "rvalue"
    #
    #         if isinstance(child, abstract_nodes.Initializer):
    #             normalized_declarator.initializer = child
    #
    #         if isinstance(child, abstract_nodes.NormalDeclarator):
    #             normalized_declarator.synthesize_from_child(child)
    #
    #     return normalized_declarator
    #
    #
    # def init_declarator(self, children):
    #     if len(children) == 1:
    #         return children[0]
    #     else:
    #         initialized_declarator = abstract_nodes.NormalDeclarator()
    #         for child in children:
    #             if isinstance(child, abstract_nodes.NormalDeclarator):
    #                 initialized_declarator.synthesize_from_child(child)
    #
    #             elif isinstance(child, abstract_nodes.Initializer):
    #                 initialized_declarator.initializer = child
    #
    #     return initialized_declarator
    #
    # ####################################################################################################################
    # # DIRECT DECLARATOR
    # def direct_declarator(self, children):
    #     normal_declarator = abstract_nodes.NormalDeclarator(children)
    #     for child in children:
    #         if isinstance(child, compiler.front_end.abstract_nodes.ast_node.ASTNode):
    #             if child.children and child.children[0].name == "IDENTIFIER":
    #                 normal_declarator.name = child.name
    #
    #     return normal_declarator
    #
    # ####################################################################################################################
    # # DECLARATION
    # def simple_declaration(self, children):
    #     decl_specs = None
    #     declarator_list = []
    #     errors = []
    #     for child in children:
    #         if isinstance(child, abstract_nodes.DeclSpec):
    #             decl_specs = child
    #         elif isinstance(child, abstract_nodes.NormalDeclarator):
    #             declarator_list.append(child)
    #
    #         # Error Checking
    #         elif isinstance(child, abstract_nodes.Error):
    #             errors.append(child)
    #
    #     normal_declaration = abstract_nodes.NormalDeclaration(decl_specs, declarator_list)
    #     for error in errors:
    #         normal_declaration.children.append(error)
    #     return normal_declaration
    #
    #
    #
    # ####################################################################################################################
    # # SUFFIXES
    #
    # def init_suffix(self, children):
    #     return children[1]
    #
    # def array_suffix(self, children):
    #     return abstract_nodes.ArraySuffix(children[0])
    #
    # def function_suffix(self, children):
    #     parameter_list = []
    #     if children and children[0].name == "parameter_list":
    #         for parameter in children[0].children:
    #             if isinstance(parameter, abstract_nodes.Parameter):
    #                 parameter_list.append(parameter)
    #
    #     return abstract_nodes.FuncSuffix(parameter_list)
    #
    # ####################################################################################################################
    # # Expression Precedence Abstraction
    # def primary(self, children):
    #     if children and len(children) == 1:
    #         if isinstance(children[0], ASTNode) and children[0].name == "literal":
    #             literal_type  = token_to_literal_kind(children[0].children[0].children[0].name)
    #             literal_value =  lexeme_to_number(children[0].children[0].name)
    #             return abstract_nodes.LiteralExpr(literal_type, literal_value)
    #
    #         # elif isinstance(children[0], ASTNode) and children[0].name == "identifier":
    #         return abstract_nodes.IdentifierExpr(children[0].children[0].name)
    #
    #         # else:
    #         #     return ASTNode("primary", children)
    #
    def unary_expression(self, children):
        # Remove Redundant Precedence
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("unary_expression", children)
    #         return abstract_nodes.UnaryExpr(children[0], children[1].name)

    def postfix_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("postfix_expression", children)
    #         return compiler.front_end.abstract_nodes.ast_node.ASTNode("postfix", children)
    #
    # def product(self, children):
    #     if len(children) == 1:
    #         return children[0]
    #     else:
    #         return abstract_nodes.BinaryExpr(children[0], children[2], children[1].name)
    #
    #
    # def sum(self, children):
    #     if children and len(children) == 1:
    #         return children[0]
    #     else:
    #         return abstract_nodes.BinaryExpr(children[0], children[2], children[1].name)
    #
    # def relational(self, children):
    #     if children and len(children) == 1:
    #         return children[0]
    #     else:
    #         return abstract_nodes.ComparisonExpr(children[0], children[2], children[1].name)
    #
    # def equality(self, children):
    #     if children and len(children) == 1:
    #         return children[0]
    #     else:
    #         return abstract_nodes.ComparisonExpr(children[0], children[2], children[1].name)
    #
    #
    # def logic_and(self, children):
    #     if children and len(children) == 1:
    #         return children[0]
    #     else:
    #         return abstract_nodes.LogicExpr(children[0], children[2], children[1].name)
    # def logic_or(self, children):
    #     if children and len(children) == 1:
    #         return children[0]
    #     else:
    #         return abstract_nodes.LogicExpr(children[0], children[2], children[1].name)





    # def cast_expression(self, children):
    #     if len(children) == 1:
    #         return children[0]
    #     else:
    #         return self
    def pm_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("pm_expression", children)
    def multiplicative_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("multiplicative_expression", children)
    def additive_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("additive_expression", children)
    def shift_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("shift_expression", children)
    def relational_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("relational_expression", children)
    def equality_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("equality_expression", children)
    def and_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("and_expression", children)
    def exclusive_or_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("exclusive_or_expression", children)
    def inclusive_or_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("inclusive_or_expression", children)
    def logical_and_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("logical_and_expression", children)
    def logical_or_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("logical_or_expression", children)
    def conditional_expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return ASTNode("conditional_expression", children)
            # return compiler.front_end.abstract_nodes.ast_node.ASTNode("conditional_expression", children)

    def assignment_expression(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("assignment_expression", children)
            # return abstract_nodes.AssignExpr(children[0], children[2], children[1].name)

    #
    # ####################################################################################################################
    # # STATEMENTS
    # def expression_statement(self, children):
    #     if children and len(children) == 1 and isinstance(children[0], compiler.front_end.abstract_nodes.base_node.Expr):
    #         return abstract_nodes.ExprStatement(children[0])
    #     else:
    #         return abstract_nodes.Error("Invalid expression statement")
    #
    # def return_statement(self, children):
    #     if len(children) == 2 and isinstance(children[1], compiler.front_end.abstract_nodes.base_node.Expr):
    #         return abstract_nodes.ReturnStatement(children[1])
    #     else:
    #         return abstract_nodes.Error("Invalid return statement")
    #
    # def compound_statement(self, children):
    #     statement_list = []
    #     for child in children:
    #         if isinstance(child, abstract_nodes.Statement):
    #             statement_list.append(child)
    #         elif isinstance(child, abstract_nodes.NormalDeclaration):
    #             statement_list.append(abstract_nodes.DeclarationStatement(child))
    #
    #         else:
    #             return abstract_nodes.Error("Non-statement in compound statement:" + str(child.name))
    #
    #     return abstract_nodes.CompoundBody(statement_list)
    #
    # def selection_statement(self, children):
    #     if len(children) == 1 and isinstance(children[0], abstract_nodes.Statement):
    #         return children[0]
    #     else:
    #         return abstract_nodes.Error("Invalid selection statement")
    #
    # def if_statement(self, children):
    #     if_condition   = children[0]
    #     then_statement = children[1]
    #     else_statement = children[2] if len(children) > 2 else None
    #
    #     return abstract_nodes.IfStatement(if_condition, then_statement, else_statement)
    #
    #
    # ####################################################################################################################
    # # ENUM / CLASS BODY
    #
    # def class_body(self, children):
    #     member_list = abstract_nodes.ClassBody()
    #     for child in children:
    #         # Found: Statement
    #         if isinstance(child, abstract_nodes.Statement):
    #             member_list.add_member(child)
    #         # Found: Access Specifier
    #
    #     return member_list
    #
    #
    # def enum_body(self, children):
    #     member_list = abstract_nodes.EnumBody()
    #
    #     # Has only-child enumerator_list
    #     if children:
    #         for enumerator in children[0].children:
    #             member_list.add_member(enumerator)
    #
    #     return member_list
    #
    #
    # ####################################################################################################################
    # # FUNCTION DEFINITION
    # def function_definition(self, children):
    #     decl_specs = children[0]
    #     declarator = children[1]
    #     compound_statement = children[2]
    #     function_definition = abstract_nodes.NormalDeclaration(decl_specs,
    #                                             [declarator],
    #                                             compound_statement,
    #                                             "function_definition")
    #     return function_definition
    #
    # ####################################################################################################################
    # # PTR -> POINTER LEVEL
    # def ptr(self, children):
    #
    #     # Initialize Empty Lists
    #     scope_path      = []
    #     type_qualifiers = []
    #
    #     # Early Return: only child = plain '*'
    #     if len(children) == 1:
    #         return abstract_nodes.PtrLevel()
    #
    #     # Check For: Scope_Qualifier Child
    #     elif isinstance(children[0],
    #                     compiler.front_end.abstract_nodes.ast_node.ASTNode) and children[0].name == "scope_qualifier":
    #         for grandchild in children[0].children:
    #             if grandchild != "::":
    #                 scope_path.append(grandchild.name)
    #
    #     # Check For: Type_Qualifier Children @ [1]
    #     if len(children) >= 2 and isinstance(children[1], compiler.front_end.abstract_nodes.ast_node.ASTNode) and children[1].name == "type_qualifier_list":
    #         for grandchild in children[1].children:
    #             type_qualifiers.append(grandchild.name)
    #
    #     # Check For: Type_Qualifier Children @ [3]
    #     elif len(children) >= 4 and isinstance(children[3], compiler.front_end.abstract_nodes.ast_node.ASTNode) and children[3].name == "type_qualifier_list":
    #         for grandchild in children[3].children:
    #             type_qualifiers.append(grandchild.name)
    #
    #     # Declare and Return PtrLevel Object
    #     return abstract_nodes.PtrLevel(scope_path, type_qualifiers)
    #


    ####################################################################################################################
