# resolve_simple_type.py

from compiler.front_end.ast_node import SimpleType, Error
from compiler.utils.scalar_size import scalar_size
from compiler.utils.valid_sets import *

def resolve_simple_type(type_seq: list[str]) -> SimpleType | Error:

        # Compute Fundamental Type
        prev_type    = None
        base_type    = None
        modifiers    = []

        for curr_type in type_seq:
            # Default to Int on modifier
            if curr_type in MODIFIER_TYPES and base_type is None:
                base_type = FundamentalTypes.INT
                modifiers.append(curr_type)

            # Check for Long_Double on Long
            if prev_type == 'long' and curr_type == 'double':
                base_type = FundamentalTypes.LONG_DOUBLE
                break

            # Manually check for Type in Enum class
            elif FundamentalTypes.__members__.get(curr_type.upper(), None) is not None:
                base_type = FundamentalTypes.__members__.get(curr_type.upper(), None)
                break

        # ERROR CHECKING: No Base Type
        if base_type is None:
            return Error("Fundamental_Type Not Found.")

        # REMOVE: Base_Type from Modifiers if it exists
        if base_type is FundamentalTypes.DOUBLE:
            modifiers.remove("double") if "double" in modifiers else None
        elif base_type is FundamentalTypes.LONG_DOUBLE:
            modifiers.remove("double") if "double" in modifiers else None
            modifiers.remove("long") if "long" in modifiers else None

        # ERROR CHECKING: base_type / is_signed
        types_found = tuple(sorted(type_seq))
        if types_found in VALID_SIMPLE_TYPE_COMBOS:

            # Check If Unsigned
            is_signed = True
            for elem in types_found:
                if elem == "unsigned":
                    is_signed = False
                    break

            # Calculate Size
            size = scalar_size(modifiers, base_type, "LLP64")

            # Construct / Return Simple Type Node
            return SimpleType(base_type, size, is_signed)

        # ERROR: Found Type Not in Valid Set
        else:
            return Error("Invalid simple type.")