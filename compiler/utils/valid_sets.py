# valid_sets.py

from enum import Enum, auto

class IdentifierIntention(Enum):
    TYPE_NAME     = auto()
    DECLARATOR_ID = auto()
    UNRESOLVED    = auto()

class FundamentalTypes(Enum):
    VOID      = auto() # Void
    BOOL      = auto() # Bool

    # Char Family
    CHAR      = auto()
    WCHAR_T   = auto()
    CHAR16_T  = auto()
    CHAR32_T  = auto()

    # Int Family
    INT        = auto()

    # Float Family
    FLOAT       = auto()
    DOUBLE      = auto()
    LONG_DOUBLE = auto()


MODIFIER_TYPES ={
    'short',
    'long',
    'double',
    'signed',
    'unsigned'
}

VALID_SIMPLE_TYPE_COMBOS = {
    # Void / Bool
    frozenset({'void'}),
    frozenset({'bool'}),

    # Chars
    frozenset({'char'}),
    frozenset({'char', 'signed'}),
    frozenset({'char', 'unsigned'}),

    # Wide/Unicode chars
    frozenset({'wchar_t'}),
    frozenset({'char16_t'}),
    frozenset({'char32_t'}),

    # Int
    frozenset({'int'}),
    frozenset({'int', 'signed'}),
    frozenset({'int', 'unsigned'}),

    # Short
    frozenset({'int', 'short'}),
    frozenset({'int', 'short', 'signed'}),
    frozenset({'int', 'short', 'unsigned'}),
    frozenset({'short'}),
    frozenset({'short', 'signed'}),
    frozenset({'short', 'unsigned'}),

    # Long
    frozenset({'int', 'long'}),
    frozenset({'int', 'long', 'signed'}),
    frozenset({'int', 'long', 'unsigned'}),
    frozenset({'long'}),
    frozenset({'long', 'signed'}),
    frozenset({'long', 'unsigned'}),

    # Long Long
    frozenset({'int', 'long', 'long'}),
    frozenset({'int', 'long', 'long', 'signed'}),
    frozenset({'int', 'long', 'long', 'unsigned'}),
    frozenset({'long', 'long'}),
    frozenset({'long', 'long', 'signed'}),
    frozenset({'long', 'long', 'unsigned'}),

    # Float / Double
    frozenset({'float'}),
    frozenset({'double'}),
    frozenset({'double', 'long'}),
}


