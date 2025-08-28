# context

from compiler.symbol_table import SymbolTable
from compiler.utils.enum_types import ScopeStack

class CompilerContext:
    def __init__(self):
        self.symbol_table = SymbolTable
        self.error_table  = []
        self.scope_tack   = ScopeStack