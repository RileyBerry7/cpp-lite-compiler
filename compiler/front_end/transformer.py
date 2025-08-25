# transformer.py
from multiprocessing.managers import Token

from lark import Lark, Transformer, Tree
from compiler.front_end.ast_node import *
from compiler.utils.literal_kind import *
from compiler.utils.lexeme_to_number import lexeme_to_number
from compiler.utils.scalar_size import scalar_size

BASE_TYPES = {'void', 'bool', 'char', 'signed', 'unsigned', 'int', 'float'}

VALID_TYPE_SETS = {
    ('void',),
    ('bool',),
    ('char',),
    ('signed',),
    ('char', 'signed'),
    ('unsigned',),
    ('char', 'unsigned'),
    ('int',),
    ('int', 'signed'),
    ('int', 'unsigned'),
    ('short',),
    ('int', 'short'),
    ('short', 'signed'),
    ('int', 'short', 'signed'),
    ('short', 'unsigned'),
    ('int', 'short', 'unsigned'),
    ('long',),
    ('int', 'long'),
    ('long', 'long'),
    ('int', 'long', 'long'),
    ('long', 'signed'),
    ('int', 'long', 'signed'),
    ('long', 'long', 'signed'),
    ('int', 'long', 'long', 'signed'),
    ('long', 'unsigned'),
    ('int', 'long', 'unsigned'),
    ('long', 'long', 'unsigned'),
    ('int', 'long', 'long', 'unsigned'),
    ('float',),
    ('double',),
    ('double', 'long'),
}

########################################################################################################################
class CSTtoAST(Transformer):
    """
    A Transformer that converts a CST to an AST.
    """

    def __default__(self, data, children, meta):
        abstract_node = ASTNode(data, children)
        return abstract_node

    def __default_token__(self, token):

        return ASTNode(token.value, [ASTNode(token.type)])


    ####################################################################################################################
    # TRANSLATION UNIT
    def translation_unit(self, children):
        return TranslationUnit(children)

    ####################################################################################################################
    # EXTERNAL DECLARATION
    def external_declaration(self, children):
        if children and isinstance(children[0], NormalDeclaration):
            return children[0]

        return Error("Invalid external declaration")

    ####################################################################################################################
    def declaration_specifier_list(self, children):

        # Initialize Empty Specs
        simple_types       = []
        elaborate_types    = []
        elaborate_name     = None
        qualifiers          = []
        storage_class      = None
        function_specifiers = []

        # Initialize Specifier Flags
        is_constexpr:   bool = False
        is_consteval:   bool = False
        is_constinit:   bool = False
        is_typedef:     bool = False
        is_using_alias: bool = False
        is_friend:      bool = False

        ################################################################################################################
        # Determine Children Names
        if children:
            for child in children:
                if isinstance(child, ASTNode):

                    # FOUND: Simple Type Specifier
                    if child.name == "simple_type_specifier":
                        simple_types.append(child.children[0].name)

                    # FOUND: Elaborate Type Specifier
                    elif child.name == "elaborated_type_specifier":

                        # SEMANTIC ERROR: multiple non-duplicate elaborate type names
                        if elaborate_name is not None and child.children[1].name == elaborate_name:
                            return Error("Multiple non-duplicate elaborate type names")
                        else:
                            # SAVE: Elaborate Type & Name
                            elaborate_type = child.children[0].name
                            elaborate_name = child.children[1].name

                    # FOUND: Type Qualifier
                    elif child.name == "type_qualifier":
                        qualifiers.append(child.children[0].name)

                    # Found: Storage Class Specifier
                    elif child.name == "storage_class_specifier":
                        # SEMANTIC ERROR: multiple storage class specifiers
                        if storage_class is not None:
                            return Error("Multiple storage class specifiers found")
                        storage_class = child.children[0].name

                    # Found: Function Specifier
                    elif child.name == "function_specifier":
                        function_specifiers.append(child.children[0].name)

                    ####################################################################################################
                    # FLAG SPECIFIER CHECKING

                    # Found:
                    elif child.name == "constexpr":
                        is_constexpr = True

                    # Found:
                    elif child.name == "consteval":
                        is_consteval = True

                    # Found:
                    elif child.name == "constinit":
                        is_constinit = True

                    # Found:
                    elif child.name == "typedef":
                        is_typedef = True

                    # Found:
                    elif child.name == "using":
                        is_using_alias = True

                    # Found:
                    elif child.name == "friend":
                        is_friend = True

        # END - Determine Children Names
        ################################################################################################################

        # Compute / Build Type Object

        # SEMANTIC ERROR: mutual exclusivity of simple_type & elaborate_type
        if elaborate_types and simple_types:
            return Error("'Elaborate' and 'Simple' types are mutually exclusive")

        # ERROR CHECKING: base_type / is_signed
        types_found = tuple(sorted(simple_types))
        if types_found in VALID_TYPE_SETS:

            # Grab base type
            if elaborate_name is not None:
                # Identifier Type Name
                base_type = elaborate_name
            else:
                # Simple Type Name
                base_type = next((t for t in types_found if t in BASE_TYPES), None)

            # Check If Unsigned
            is_signed = True
            for elem in types_found:
                if elem == "unsigned":
                    is_signed = False
                    break

            # Calculate Size
            if elaborate_types:
                size = None
                print("\033[93;5;28mWarning: Found elaborate type, memory size uncertain.\n"
                      + str(elaborate_types) + "\033[0m")
            else:
                size = scalar_size(types_found, base_type, "LLP64")

            # Compile Type Node
            type_node = Type(' '.join(types_found), base_type, size, is_signed, elaborate_types)

        # ERROR: Found Type Not in Valid Set
        else:
            return Error("Invalid type specifier found.")

        # Create and Return Declaration Specifier Node
        specifier_node = DeclSpec(type_node, qualifiers, storage_class, function_specifiers)

        # Set Bool-Flag Specifiers
        specifier_node.is_constexpr   = is_constexpr
        specifier_node.is_consteval   = is_consteval
        specifier_node.is_constinit   = is_constinit
        specifier_node.is_typedef     = is_typedef
        specifier_node.is_using_alias = is_using_alias
        specifier_node.is_friend      = is_friend


        # Return Declaration Specs Node
        return specifier_node

    ####################################################################################################################
    # PARAMETER
    def parameter(self, children):

        param_declaration = children[0]
        default_args = None




        return Parameter(param_declaration, default_args)

    def default_arg(self, children):
            if len(children) >= 1 and isinstance(children[1], Initializer):
                return children[1]
            else:
                return Error("No Initializer Found for Default Argument")


    def initializer(self, children):
        for child in children:
            if isinstance(child, ASTNode):
                if isinstance(child, Expr):
                    return Initializer(child)

                if isinstance(child, Initializer):
                    return child

    ####################################################################################################################
    # DECLARATOR
    def declarator(self, children):
        normalized_declarator = NormalDeclarator()
        for child in children:
            if isinstance(child, ASTNode) and child.name == "ptr_list":
                for ptr_lvl in child.children:
                    if isinstance(ptr_lvl, PtrLevel):
                        normalized_declarator.ptr_chain.append(ptr_lvl) # Might be backwards!!!

            if isinstance(child, ASTNode) and child.name == "reference_operator":
                if children.children and child.children[0].name == "AND":
                    normalized_declarator.reference = "lvalue"
                else:
                    normalized_declarator.reference = "rvalue"

            if isinstance(child, Initializer):
                normalized_declarator.initializer = child

            if isinstance(child, NormalDeclarator):
                normalized_declarator.synthesize_from_child(child)

        return normalized_declarator


    def init_declarator(self, children):
        if len(children) == 1:
            return children[0]
        else:
            initialized_declarator = NormalDeclarator()
            for child in children:
                if isinstance(child, NormalDeclarator):
                    initialized_declarator.synthesize_from_child(child)

                elif isinstance(child, Initializer):
                    initialized_declarator.initializer = child

        return initialized_declarator

    ####################################################################################################################
    # DIRECT DECLARATOR
    def direct_declarator(self, children):
        normal_declarator = NormalDeclarator(children)
        for child in children:
            if isinstance(child, ASTNode):
                if child.children and child.children[0].name == "IDENTIFIER":
                    normal_declarator.name = child.name

        return normal_declarator

    ####################################################################################################################
    # DECLARATION
    def declaration(self, children):
        decl_specs = None
        declarator_list = []
        errors = []
        for child in children:
            if isinstance(child, DeclSpec):
                decl_specs = child
            elif isinstance(child, NormalDeclarator):
                declarator_list.append(child)

            # Error Checking
            elif isinstance(child, Error):
                errors.append(child)

        normal_declaration = NormalDeclaration(decl_specs, declarator_list)
        for error in errors:
            normal_declaration.children.append(error)
        return normal_declaration



    ####################################################################################################################
    # SUFFIXES

    def init_suffix(self, children):
        return children[1]

    def array_suffix(self, children):
        return ArraySuffix(children[0])

    def function_suffix(self, children):
        parameter_list = []
        if children and children[0].name == "parameter_list":
            for parameter in children[0].children:
                if isinstance(parameter, Parameter):
                    parameter_list.append(parameter)

        return FuncSuffix(parameter_list)

    ####################################################################################################################
    # Expression Precedence Abstraction
    def primary(self, children):
        if children and len(children) == 1:
            if isinstance(children[0], ASTNode) and children[0].name == "literal":
                literal_type  = token_to_literal_kind(children[0].children[0].children[0].name)
                literal_value =  lexeme_to_number(children[0].children[0].name)
                return LiteralExpr(literal_type, literal_value)

            # elif isinstance(children[0], ASTNode) and children[0].name == "identifier":
            return IdentifierExpr(children[0].children[0].name)

            # else:
            #     return ASTNode("primary", children)

    def unary(self, children):
        # Remove Redundant Precedence
        if children and len(children) == 1:
            return children[0]
        else:
            return UnaryExpr(children[0], children[1].name)

    def postfix(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("postfix", children)

    def product(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return BinaryExpr(children[0], children[2], children[1].name)


    def sum(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return BinaryExpr(children[0], children[2], children[1].name)

    def relational(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ComparisonExpr(children[0], children[2], children[1].name)

    def equality(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ComparisonExpr(children[0], children[2], children[1].name)


    def logic_and(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return LogicExpr(children[0], children[2], children[1].name)
    def logic_or(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return LogicExpr(children[0], children[2], children[1].name)

    def conditional_expression(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return ASTNode("conditional_expression", children)

    def assignment_expression(self, children):
        if children and len(children) == 1:
            return children[0]
        else:
            return AssignExpr(children[0], children[2], children[1].name)


    ####################################################################################################################
    # STATEMENTS
    def expression_statement(self, children):
        if children and len(children) == 1 and isinstance(children[0], Expr):
            return ExprStatement(children[0])
        else:
            return Error("Invalid expression statement")

    def return_statement(self, children):
        if len(children) == 2 and isinstance(children[1], Expr):
            return ReturnStatement(children[1])
        else:
            return Error("Invalid return statement")

    def compound_statement(self, children):
        statement_list = []
        for child in children:
            if isinstance(child, Statement):
                statement_list.append(child)
            elif isinstance(child, NormalDeclaration):
                statement_list.append(DeclarationStatement(child))

            else:
                return Error("Non-statement in compound statement:" + str(child.name))

        return CompoundStatement(statement_list)

    def selection_statement(self, children):
        if len(children) == 1 and isinstance(children[0], Statement):
            return children[0]
        else:
            return Error("Invalid selection statement")

    def if_statement(self, children):
        if_condition   = children[0]
        then_statement = children[1]
        else_statement = children[2] if len(children) > 2 else None

        return IfStatement(if_condition, then_statement, else_statement)


    ####################################################################################################################
    # FUNCTION DEFINITION
    def function_definition(self, children):
        decl_specs = children[0]
        declarator = children[1]
        compound_statement = children[2]
        function_definition = NormalDeclaration(decl_specs, [declarator], compound_statement)
        function_definition.name = "\x1b[1;38;2;80;160;255mfunction_definition\x1b[0m"
        return function_definition

    ####################################################################################################################
    # PTR -> POINTER LEVEL
    def ptr(self, children):

        # Initialize Empty Lists
        scope_path      = []
        type_qualifiers = []

        # Early Return: only child = plain '*'
        if len(children) == 1:
            return PtrLevel()

        # Check For: Scope_Qualifier Child
        elif isinstance(children[0], ASTNode) and children[0].name == "scope_qualifier":
            for grandchild in children[0].children:
                if grandchild != "::":
                    scope_path.append(grandchild.name)

        # Check For: Type_Qualifier Children @ [1]
        if len(children) >= 2 and isinstance(children[1], ASTNode) and children[1].name == "type_qualifier_list":
            for grandchild in children[1].children:
                type_qualifiers.append(grandchild.name)

        # Check For: Type_Qualifier Children @ [3]
        elif len(children) >= 4 and isinstance(children[3], ASTNode) and children[3].name == "type_qualifier_list":
            for grandchild in children[3].children:
                type_qualifiers.append(grandchild.name)

        # Declare and Return PtrLevel Object
        return PtrLevel(scope_path, type_qualifiers)



    ####################################################################################################################
