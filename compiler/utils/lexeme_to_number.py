# lexeme_to_number.py

import math

def lexeme_to_number(lexeme: str) -> int | float | str:

    # try integer first (base=0 allows 0x..., 0o..., 0b...)
    try:
        return int(lexeme, 0)
    except ValueError:
        pass

    # then float
    try:
        x = float(lexeme)
        if not math.isfinite(x):           # reject inf/nan
            return lexeme
        return int(x) if x.is_integer() else x
    except ValueError:
        return lexeme

