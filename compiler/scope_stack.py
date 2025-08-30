# scopy_stack.py

from __future__ import annotations
from compiler.utils.enum_types import ScopeKind

#############################################################################################################3##########
# SCOPE

class Scope:
    def __init__(self, kind: ScopeKind, scope_id:int, parent: Scope | None = None):
        self.kind    = kind
        self.id      = scope_id
        self.parent  = parent  or None # Scope which contains this scope (Outer Scope)
        self.symbols = {}              # Dict of {symbol_name: symbol_id}

#############################################################################################################3##########
# SCOPE STACK

class ScopeStack:
    def __init__(self):
        self.scopes = []
        self.next_id = 0  # Unique identifier for symbols
        self.curr_scope: Scope | None = None

    def enter_scope(self, kind:ScopeKind):

        # Create New Scope
        new_scope = Scope(kind, self.next_id, self.curr_scope)
        self.scopes.append(new_scope)  # Push to Scope Stack
        self.curr_scope = new_scope    # Update Current Scope
        self.next_id += 1              # Increment ID
        print("Entered Scope:", new_scope.kind.name)

    def exit_scope(self):
        print("Exited Scope:", self.curr_scope.kind.name)
        if len(self.scopes) > 1:
            self.curr_scope = self.curr_scope.parent
        self.scopes.pop()


    # def resolve_scope(self):
#############################################################################################################3##########
