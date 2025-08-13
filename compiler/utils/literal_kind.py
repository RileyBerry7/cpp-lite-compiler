# literal_kind.py
from enum import Enum, unique


@unique
class LiteralKind(str, Enum):
    INT     = "INT"
    FLOAT   = "FLOAT"
    CHAR    = "CHAR"
    STRING  = "STRING"
    BOOL    = "BOOL"
    NULLPTR = "NULLPTR"

token_mapping = {
    "INT_LITERAL"    : LiteralKind.INT,
    "FLOAT_LITERAL"  : LiteralKind.FLOAT,
    "CHAR_LITERAL"   : LiteralKind.CHAR,
    "STRING_LITERAL" : LiteralKind.STRING,
    "BOOL_LITERAL"   : LiteralKind.BOOL,
    "NULLPTR_LITERAL": LiteralKind.NULLPTR
}

def token_to_literal_kind(token_type:str) -> LiteralKind:
    mapped_literal = token_mapping.get(token_type)
    if mapped_literal is None:
        raise ValueError(f"Unknown token type: {token_type}")
    return mapped_literal