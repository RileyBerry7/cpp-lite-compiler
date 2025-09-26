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
from compiler.utils.valid_sets import IdentifierIntention


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
                path.ansi_color = colors.red.italic
                branches.append(path)
        ambig_node = abstract_nodes.ASTNode("Ambiguity", branches)
        ambig_node.ansi_color = colors.red.underline.italic
        return ambig_node

    ####################################################################################################################
    def translation_unit(self, children):
        return ASTNode("translation_unit", children, colors.blue.underline)

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
        if len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("type_specifier")

    #####################################################################################################################
    def trailing_type_specifier(self, children):
        # Collapse on Only-Child
        if len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("trailing_type_specifier")

    ######################################################################################################################
    # SIMPLE_TYPE_SPECIFIER

    def simple_type_specifier(self, children):
        # Collapse on Only-Child
        if len(children) == 1:
            return children[0]
        else:
            return abstract_nodes.Error("simple_type_specifier", children)

    ######################################################################################################################
    # TYPE_NAME
    def type_name(self, children):
        # Collapse on Only-Child
        if len(children) == 1:
            # Link Identifier Intention (Decoration)
            first_child = children[0]
            if isinstance(first_child, abstract_nodes.Identifier):
                first_child.update_intent(IdentifierIntention.TYPE_NAME)
            return first_child
        else:
            return abstract_nodes.Error("type_name")

    ######################################################################################################################
    # DECLARATOR_NAME
    def declarator_name(self, children):
        # Collapse on Only-Child
        if len(children) == 1:
            # Link Identifier Intention (Decoration)
            first_child = children[0]
            if isinstance(first_child, abstract_nodes.Identifier):
                first_child.update_intent(IdentifierIntention.DECLARATOR_NAME)
            return first_child
        else:
            return abstract_nodes.Error("declarator_name")

    # ####################################################################################################################
    # DECLARATOR SUFFIXES

    # def declarator_suffix(self, children):
    #     # FUlly Collapse
    #     return children[0]

    def array_suffix(self, children):

        if len(children) == 1:
            return abstract_nodes.ArraySuffix(children[0])
        else:
            return abstract_nodes.ArraySuffix()

    # function_suffix: parameters_and_qualifiers

    # parameters_and_qualifiers: _LPAREN parameter_declaration_clause _RPAREN attribute_specifier? cv_qualifier_seq? \
    #                        ref_qualifier? excieption_specification?

    #     parameter_declaration_clause: parameter_declaration_list? ELLIPSIS?
    #                                 | parameter_declaration_list _COMMA ELLIPSIS

    # parameter_declaration_list: parameter_declaration (_COMMA parameter_declaration)* # <- Right-Recursion Eliminated
    def function_suffix(self, children):
        # Fully Collapse
        return children[0]

    def parameters_and_qualifiers(self, children):
        if children[0] and isinstance(children[0], ASTNode)  and children[0].name == "parameter_list":
            return abstract_nodes.FunctionSuffix(children[0])
        else:
            return abstract_nodes.FunctionSuffix()

    def parameter_declaration_clause(self, children):
        for c in children:
            if isinstance(c, ASTNode):
                if c.name == "parameter_declaration_list":
                    return abstract_nodes.Body[ASTNode]("parameter_list", c.children)

        return abstract_nodes.Error("parameter_declaration_clause")

    #####################################################################################################################
    # BODIES
    def function_body(self, children):
        if children:
            first_child = children[0]
            if len(children) == 1 and isinstance(first_child, abstract_nodes.Body):
                first_child.name = "function_body"
                return first_child
        return abstract_nodes.Error("function_body")

    ######################################################################################################################

    def statement(self, children):
        # Fully Collapse
        return children[0]

    ####################################################################################################################

    def compound_statement(self, children):
        # Fully Collapse
        return children[0]

    def statement_seq(self, children):
        stmt_seq = abstract_nodes.Body[ASTNode]("statement_sequence")
        for child in children:
            stmt_seq.add_member(child)
        return stmt_seq
    #####################################################################################################################
    #

    #####################################################################################################################
    # IDENTIFIER WRAPPERS

    def ambiguous_identifier(self, children):
        return abstract_nodes.AmbigIdentifer(children[0])

    def declarator_id(self, children):
        # Fully Collapse
        return children[0]

    def qualified_id(self, children):
        # Fully Collapse
        return children[0]

    def unqualified_id(self, children):
        # Fully Collapse
        return children[0]

    #####################################################################################################################
    # PRIMARY EXPRESSIONS

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

    # def postfix_expression(self, children):
    #
    #     # Resolve Expression Precedence
    #     if len(children) == 1 and isinstance(children[0], ASTNode):
    #         return children[0]
    #     else:
    #         return abstract_nodes.Error("postfix_expression", children)

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

    #####################################################################################################################
    # EXPRESSION WRAPPERS (No Precedence)
    def expression(self, children):
        # Fully Collapse
        return children[0]

    def constant_expression(self, children):
        # Fully Collapse
        return abstract_nodes.ConstantExpr(children[0])




