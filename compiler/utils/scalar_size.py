# scalar_size.py

from compiler.utils.valid_sets import *

def scalar_size(specs: list[str], base_type: FundamentalTypes, model="LP64"):
    """
    specs: iterable of modifiers like ["signed","long","long"].
    base_type: "int" | "char" | "wchar_t" | "char16_t" | "char32_t"
               | "bool" | "float" | "double" | "long double"
    model: "LP64" (Linux/macOS 64-bit) or "LLP64" (Windows 64-bit)
    Returns size in bits.
    """
    specs = list(specs)
    nlong = specs.count("long")
    has_short = "short" in specs

    # Floats
    if base_type == FundamentalTypes.FLOAT:         return 32
    if base_type == FundamentalTypes.DOUBLE:        return 64
    if base_type == FundamentalTypes.LONG_DOUBLE:   return 80 if model == "LP64" else 64

    # Bool / char family
    if base_type == FundamentalTypes.BOOL:          return 8
    if base_type == FundamentalTypes.CHAR:          return 8
    if base_type == FundamentalTypes.WCHAR_T:
        return 32 if model == "LP64" else 16
    if base_type == FundamentalTypes.CHAR16_T:      return 16
    if base_type == FundamentalTypes.CHAR32_T:      return 32

    # Integers (signed/unsigned don't change size)
    if has_short:
        if nlong:
            raise ValueError("invalid: short with long")
        return 16

    if nlong >= 2:   # long long
        return 64
    if nlong == 1:   # long
        return 64 if model == "LP64" else 32

    # plain int
    return 32
