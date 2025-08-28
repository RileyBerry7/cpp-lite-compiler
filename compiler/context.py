# context

from compiler.symbol_table import SymbolTable
from compiler.scope_stack  import ScopeStack
from compiler.error_table  import DiagnosticEngine

class CompilerContext:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.error_table  = DiagnosticEngine()
        self.scope_tack   = ScopeStack()