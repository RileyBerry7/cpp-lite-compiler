# context

from dataclasses import dataclass
from compiler.symbol_table import SymbolTable
from compiler.scope_stack  import ScopeStack
from compiler.error_table  import DiagnosticEngine

@dataclass
class CompilerContext:
    symbol_table = SymbolTable()
    error_table  = DiagnosticEngine()
    scope_stack   = ScopeStack()