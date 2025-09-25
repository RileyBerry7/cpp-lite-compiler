# transformer.py
import lark
from lark import Transformer

from compiler.context import CompilerContext
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
    # PASS 1
    def disambiguate(self, cst_root):
        from compiler.front_end.disambiguator import Disambiguator
        disambiguator = Disambiguator()
        new_root = disambiguator.transform(cst_root)
        return new_root

    # PASS 3
    # def secondary_transform(self, ast_root: ASTNode, context: CompilerContext) -> ASTNode:
    #     from compiler.front_end.secondary_transform import SecondaryTransform
    #     transformation_pass = SecondaryTransform(ast_root, context)
    #     transformation_pass.walk()
    #     return ast_root


    # PASS 2
    ####################################################################################################################
    def __default__(self, data, children, meta):
        return ASTNode(data, children)

    ####################################################################################################################
    def __default_token__(self, token):
        from compiler.front_end.disambiguator import keywords, operators
        if token.type == "IDENTIFIER":
            return abstract_nodes.Identifier(token.value)
        elif token.value in keywords:
            return abstract_nodes.Keyword(token.value)
        elif token.value in operators:
            return abstract_nodes.Operator(token.value)
        else:
            return ASTNode(token.type, [ASTNode(token.value)])

    ####################################################################################################################
    # Ambiguous Nodes
    def _ambig(self, possible_trees):
        from compiler.utils.colors import colors

        # Ambiguity Resolved
        if len(possible_trees) == 1:
            true_branch = possible_trees[0]
            if isinstance(true_branch, ASTNode):
                true_branch.ansi_color = colors.green
                return true_branch
            else:
                return abstract_nodes.Error("Ambiguity resolved into none.")

        # Ambiguity Unresolved
        branches = []
        for path in possible_trees:
            if isinstance(path, abstract_nodes.ASTNode):
                path.ansi_color = colors.orange
                branches.append(path)
        ambig_node = abstract_nodes.ASTNode("Ambiguity", branches)
        ambig_node.ansi_color = colors.red.underline
        return ambig_node

    ####################################################################################################################
    # ptr_operator: STAR attribute_specifier? cv_qualifier_seq?
    #             | BIT_AND attribute_specifier?
    #             | AND attribute_specifier?
    #             | SCOPE? nested_name_specifier STAR attribute_specifier? cv_qualifier_seq?
    def ptr_operator(self, children):
        for c in children:
            # FOUND: Chain Start
            if isinstance(c, abstract_nodes.Operator):
                chain_start = c

            # FOUND: CV_Qualifier_Sequence
            elif isinstance(c, ASTNode) and c.name == "cv_qualifier_seq":
                    for k in c.children:
                        if chain_start:
                            chain_start.children.append(k)

        # RETURN: Chain Start or Error
        return chain_start if chain_start else abstract_nodes.Error("Invalid ptr_operator")

    ####################################################################################################################
    def cv_qualifier(self, children):
        if len(children) == 1 and isinstance(children[0], ASTNode):
            return children[0]
        else:
            return abstract_nodes.Error("cv_qualifier")

    ####################################################################################################################
    def literal(self, children):
        kind = get_kind(children[0].name)
        value = children[0].children[0].name
        return abstract_nodes.Literal(kind, value)

    ####################################################################################################################

    def block_declaration(self, children):
        return children[0]

    def declaration(self, children):
        return children[0]

    def declaration_seq(self, children):
        return children[0]

    # ####################################################################################################################
    # type_specifier_seq:
    def type_specifier_seq(self, children):
        # TYPE CORE DEDUCTION

        # BuiltInType Core
        if children and all(isinstance(c, abstract_nodes.Keyword) for c in children):
            keywords = [c.lexeme for c in children]
            return resolve_simple_type(keywords)

        # Other Core
        else:
            return ASTNode("type_specifier_seq", children)

    #####################################################################################################################
    # type_specifier: trailing_type_specifier  # also wraps simple_type_specifier
    #               | class_specifier
    #               | enum_specifier
    def type_specifier(self, children):
        # Collapse on Only-Child
        for child in children:
            if isinstance(child, abstract_nodes.Keyword):
                return child
        return ASTNode("type_specifier", children)

    #####################################################################################################################
    def trailing_type_specifier(self, children):
        for child in children:
            if isinstance(child, abstract_nodes.Keyword):
                return child
        return ASTNode("trailing_type_specifier", children)
    #
    # #####################################################################################################################
    # # simple_type_specifier:
    def simple_type_specifier(self, children):
        for child in children:
            if isinstance(child, abstract_nodes.Keyword):
                return child
        return ASTNode("simple_type_specifier", children)

    # ####################################################################################################################
    # DECLARATOR SUFFIXES
    # def array_suffix(self, children):
    #     return abstract_nodes.ArraySuffix(children[0])

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

    #####################################################################################################################
    # PRIMARY EXPRESSIONS

    def unqualified_id(self, children):
        # Fully Collapse
        return children[0]

    def id_expression(self, children):
        # Fully Collapse
        return children[0]

    def primary_expression(self, children):
        if len(children) == 1 and isinstance(children[0], ASTNode):
            return children[0]
        else:
            return abstract_nodes.Error("primary_expression")

    #####################################################################################################################
    # UNARY EXPRESSION

    def postfix_expression(self, children):

        # Resolve Expression Precedence
        if len(children) == 1 and isinstance(children[0], ASTNode):
            return children[0]
        else:
            return abstract_nodes.Error("postfix_expression")

    def unary_expression(self, children):

        # Resolve Expression Precedence
        if len(children) == 1 and isinstance(children[0], ASTNode):
            return children[0]
        else:
            return abstract_nodes.Error("primary_expression")


    #####################################################################################################################
    # CAST EXPRESSION

    # cast_expression: unary_expression
    #            | _LPAREN type_id _RPAREN cast_expression # C Style Cast   (int)var;
    #                                                      # C++ Style Cast int(var); <- includes: static, constant, dynamic, reinterpret
    def cast_expression(self, children):

        if len(children) == 2:
            return abstract_nodes.CastExpr(children[0], children[1])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("cast_expression")

    #####################################################################################################################
    #  MEMBER ACCESS EXPRESSION

    # pm_expression: cast_expression
    #              | pm_expression DOT_STAR   cast_expression
    #              | pm_expression ARROW_STAR cast_expression
    def pm_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.MemberAccess(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("pm_expression")

    #####################################################################################################################
    # BINARY EXPRESSIONS

    # multiplicative_expression: pm_expression
    #                          | multiplicative_expression STAR pm_expression
    #                          | multiplicative_expression SLASH pm_expression
    #                          | multiplicative_expression PERCENT pm_expression
    def multiplicative_expression(self, children):
        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("multiplicative_expression")

    # additive_expression: multiplicative_expression
    #                    | additive_expression PLUS multiplicative_expression
    #                    | additive_expression MINUS multiplicative_expression
    def additive_expression(self, children):
        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("additive_expression")

    # shift_expression: additive_expression
    #                 | shift_expression SHL additive_expression
    #                 | shift_expression SHR additive_expression
    def shift_expression(self, children):
        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("shift_expression")

    # relational_expression: shift_expression
    #                      | relational_expression LT shift_expression
    #                      | relational_expression GT shift_expression
    #                      | relational_expression LE shift_expression
    #                      | relational_expression GE shift_expression
    def relational_expression(self, children):
        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("relational_expression")

    # equality_expression: relational_expression
    #                    | equality_expression EQ relational_expression
    #                    | equality_expression NEQ relational_expression
    def equality_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("equality_expression")

    # and_expression: equality_expression
    #               | and_expression BIT_AND equality_expression
    def and_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("and_expression")

    # exclusive_or_expression: and_expression
    #                        | exclusive_or_expression BIT_XOR and_expression
    #
    def exclusive_or_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("exclusive_or_expression")

    # inclusive_or_expression: exclusive_or_expression
    #                        | inclusive_or_expression BIT_OR exclusive_or_expression
    def inclusive_or_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.BinaryExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("inclusive_or_expression")

    #####################################################################################################################
    # LOGIC EXPRESSIONS

# logical_and_expression: inclusive_or_expression
#                       | logical_and_expression AND inclusive_or_expression
    def logical_and_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.LogicExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("logical_and_expression")

    # logical_or_expression: logical_and_expression
    #                  | logical_or_expression OR logical_and_expression
    def logical_or_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.LogicExpr(children[0], children[1], children[2])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("logical_or_expression")

    #####################################################################################################################
    # CONDITIONAL EXPRESSIONS

# conditional_expression: logical_or_expression
#                       | logical_or_expression TERNARY expression COLON assignment_expression
    def conditional_expression(self, children):

        if len(children) == 4:
            return abstract_nodes.ConditionalExpr(children[0], children[2], children[3])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("conditional_expression")

    #####################################################################################################################
    # ASSIGNMENT EXPRESSIONS

# assignment_expression: conditional_expression
#                      | logical_or_expression assignment_operator initializer_clause
#                      | throw_expression
    def assignment_expression(self, children):

        if len(children) == 3:
            return abstract_nodes.AssignExpr(children[0], children[2], children[1])
        elif len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("assignment_expression")

