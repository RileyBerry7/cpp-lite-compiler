def scalar_size(specs, base_type, model="LP64"):
    """
    specs: iterable of modifiers like ["signed","long","long"].
    base_type: "int" | "char" | "bool" | "float" | "double" | "long double"
    model: "LP64" (Linux/macOS 64-bit) or "LLP64" (Windows 64-bit)
    Returns size in bits.
    """
    specs = list(specs)
    nlong = specs.count("long")
    has_short = "short" in specs

    # floats first
    if base_type == "float":         return 32
    if base_type == "double":        return 64
    if base_type == "long double":   return 80 if model == "LP64" else 64

    # char/bool
    if base_type in ("char", "bool"):
        return 8

    # integers (signed/unsigned don't change size)
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
