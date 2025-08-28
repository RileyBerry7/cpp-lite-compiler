# error_table.py

from enum import Enum, auto
from dataclasses import dataclass
from compiler.utils.data_classes import SourceLocation

####################################################################################################################
class Severity(Enum):
    ERROR   = auto()
    WARNING = auto()
    NOTE    = auto()

####################################################################################################################
class ErrorKind(Enum):
    """
    Notes:
        Forward-declarations allowed for Tags & Functions

    """

    # 0. NORMALIZATION PASS:
    DUPLICATE_TYPE_QUALIFIER = auto #
    STORAGE_CLASS_CONFLICT   = auto #

    # 1. SYMBOL COLLECTION PASS: builds scope_stack / populates symbol_table
    # (Core Conflict Issues):
    CONFLICTING_DECLARATION     = auto() # int foo; double foo; <- identical identifier used in invalid scope / ns
    REDECLARATION               = auto() # Identical declaration on forward-declaration invalid type.
    CONFLICTING_PARAMETER       = auto() # same name, diff-type. void foo(int a, float a);
    PARAMETER_REDECLARATION     = auto() # void foo(int b, int b); <- Identical signature
    FUNCTION_OVERLOAD_COLLISION = auto() # void f(int); void f(int); <- Identical Signature
    # (Tag Issues):
    MULTIPLE_TAG_BODIES   = auto() # struct A {} a, struct B {} b; <- Single Decleration
    TAG_REDEFINITION            = auto() # Tag with multiple bodies. struct A{...}; struct A{...}
    DUPLICATE_TAG_MEMBER        = auto() # Tag (struct, class, union, enum) member
    # (Name & Scope Issues):
    DUPLICATE_LABEL             = auto() # goto L; L: ; L: ;
    ILLEGAL_SHADOWING           = auto() # Inner declaration hides outer (warn/error)
    ENUM_INJECTION_CONFLICT     = auto() # (unscoped) Enum member conflicts with declaration from outer-scope
    UNION_INJECTION_CONFLICT    = auto() # (anonymous) Union declaration conflict with prior Anon-Union
    ALIAS_REBIND_CONFLICT       = auto() # Failed namespace alias rebind
    # (Template Issues):
    DUPLICATE_TEMPLATE_PARAMETER= auto() # template <typename T, typename T>


    # 2. SYMBOL BINDING PASS: finds valid def on use.
    UNDECLARED_IDENTIFIER   = auto() # Use of undeclared variable/function
    AMBIGUOUS_REFERENCE     = auto() # Multiple visible matches, cannot resolve
    ACCESS_VIOLATION        = auto() # Invalid access (private/protected)
    NAMESPACE_MEMBER_MISSING= auto() # No such member in namespace/qualifier
    INCOMPLETE_TYPE_USE     = auto() # Forward-declared/incomplete type used illegally
    INVALID_STATIC_CONTEXT  = auto() # Use of non-static member without `this`
    QUALIFIER_NOT_NAMED_SCOPE = auto() #
    NOT_A_TYPE_NAME         = auto() #
    MISSING_TYPE_NAME       = auto() #
    MEMBER_ACCESS_ON_NON_CLASS = auto() #
    NO_MATCHING_OVERLOAD = auto() #






####################################################################################################################

# Message catalog
MESSAGE_TEMPLATES = {
    ErrorKind.REDECLARATION: "Redeclaration of '{name}'",
    ErrorKind.UNDECLARED_IDENTIFIER: "Use of undeclared identifier '{name}'",
    # ErrorKind.TYPE_MISMATCH: "Incompatible types: {lhs} vs {rhs}",
}
####################################################################################################################

# Diagnostic Entry
@dataclass
class Diagnostic:
    severity: Severity
    kind: ErrorKind
    loc: tuple[str, int, int]  # (filename, line, col)
    args: dict                 # e.g., {"lhs": "int", "rhs": "float"}

####################################################################################################################
class DiagnosticEngine:
    def __init__(self):
        self.entries: list[Diagnostic] = []

    def report(self, kind: ErrorKind, severity: Severity, loc, **kwargs):
        self.entries.append(Diagnostic(severity, kind, loc, kwargs))

    def dump(self):
        for diag in self.entries:
            template = MESSAGE_TEMPLATES[diag.kind]
            msg = template.format(**diag.args)
            file, line, col = diag.loc
            print(f"{file}:{line}:{col}: {diag.severity.name.lower()}: {msg}")

####################################################################################################################