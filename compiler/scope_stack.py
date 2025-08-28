# scopy_stack.py

from __future__ import annotations
from compiler.utils.enum_types import ScopeKind

class Scope:
    def __init__(self, kind: ScopeKind, scope_id:int, parent: "Scope" | None = None):
        self.kind    = ScopeKind
        self.id      = scope_id
        self.parent  = parent  or None # Scope which contains this scope (Outer Scope)
        self.symbols = {}              # Dict of {symbol_name: symbol_id}

class ScopeStack:
    def __init__(self):
        self.scopes = []
        self.next_id = 0  # Unique identifier for symbols
        self.curr_scope = Scope(ScopeKind.File, self.next_id, None)

        # Initial Scope
        self.scopes.append(self.curr_scope)

    def enter_scope(self, scope_kind:str):

        self.next_id += 1 # Increment ID

        # Create New Scope
        new_scope = Scope(ScopeKind[scope_kind.upper()], self.next_id, self.curr_scope)
        self.scopes.append(new_scope)  # Push to Scope Stack
        self.curr_scope = new_scope    # Update Current Scope


    # def exit_scope(self):

    # def resolve_scope(self):
