# declaration_nodes.py

from compiler.front_end.abstract_nodes.ast_node import ASTNode
from compiler.front_end.abstract_nodes.base_node import *
from compiler.utils.colors import colors

##########################################################################################
""" C++ Declaration Types:
        - SymbolBound:
               VariableDeclaration -> memory container
                      ParameterDeclaration
                      EnumeratorDeclaration

               FunctionDeclaration -> callable container
                      (optional_body)

               NamespaceDeclaration -> scope container
                      (required_body)

               TypeDeclaration -> type alias
                      TypeDef
                      ClassDeclaration
                            (optional_body)
                      EnumDeclaration
                            (optional_body)

        - Anonymous:
               UsingDeclaration  -> scope injector
               FriendDeclaration -> access injector

        """
##########################################################################################
# Base Declaration Type: 1st Generation
class Declaration(ASTNode):
    def __init__(self, declaration_specs: DeclSpec, declaration_type: str = "declaration"):
        super().__init__(node_name=declaration_type)
        self.decl_specs = declaration_specs


##########################################################################################
# Symbol/Identifier Families: Second Generation

class BoundDeclaration(Declaration):
    def __init__(self,
                 decl_specs: DeclSpec,
                 identifier_name: str,
                 decl_type: str = "bound_declaration"):
        super().__init__(decl_specs=decl_specs, declaration_type=decl_type)
        self.identifier = identifier_name
        self.symbol = None


class AnonDeclaration(Declaration):
    def __init__(self, decl_specs: DeclSpec, decl_type: str = "anonymous_declaration"):
        super().__init__(declaration_specs=decl_specs, decl_type=)


##########################################################################################
# Bounded Children: Second Generation

class VariableDeclaration(BoundDeclaration):
    def __init__(self, specs: DeclSpec, identifier: str, sub_type: str = "variable_declaration"):
        super().__init__(decl_specs=specs, identifier_name=identifier, decl_type=sub_type)
        self.type_specs = None
        self.storage_class = None  # Optional
        self.initializer = None  # Optional


class FunctionDeclaration(BoundDeclaration):
    def __init__(self, specs: DeclSpec, identifier: str):
        super().__init__(decl_specs=specs, identifier_name=identifier, decl_type="")
        return_type
        storage_class
        name
        parameters
        body


class NamespaceDeclaration(BoundDeclaration):
    def __init__(self, specs: DeclSpec, identifier: str):
        super().__init__(decl_specs=specs, identifier_name=identifier, decl_type="")
        name
        body  # list of declarations





##########################################################################################
# Variable Subtypes: Fourth Generation

class ParameterDeclaration(VariableDeclaration):
    def __init__(self, specs: DeclSpec, identifier: str):
        super().__init__(specs=specs, identifier=identifier, sub_type="")
        self.is_variadic: bool = False


class EnumeratorDeclaration(VariableDeclaration):
    def __init__(self, specs: DeclSpec, identifier: str):
        super().__init__(specs=specs, identifier=identifier, sub_type="")
        self.is_variadic: bool = False
##########################################################################################
# 3rd Generation Base
class TypeDeclaration(BoundDeclaration):
    def __init__(self, specs: DeclSpec, identifier: str):
        super().__init__(decl_specs=specs, identifier_name=identifier, decl_type="")
        self.body: Body | None = None
        self.can_have_body = False

# 4th Generation Subtypes
class TypeDefinition(TypeDeclaration):
    def __init__(self):
        super().__init__()
        self.aliased_type: SimpleType | ElaborateType

class ClassDeclaration(TypeDeclaration):
    def __init__(self, body: ClassBody):
        super().__init__()
        self.class_type = None
        self.class_body = body

class EnumDeclaration(TypeDeclaration):
    def __init__(self, body: EnumBody):
        super().__init__()
        self.enum_body = body
        self.is_scoped = None
        self.underlying_type = None

##########################################################################################



##########################################################################################

