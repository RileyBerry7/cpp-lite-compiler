from multiprocessing.managers import Token

from lark import Tree


########################################################################################################################
class ASTtoDAST:
    """
    A class that will decorate the AST with LLVM IR relevant semantic information. The decoration process will
    recursively travers the AST and fully create a decorated version of it using the DecNode class instead of
    the lark tree class.
    """
    def __init__(self):
        self.error_table = []
        self.symbol_table = {}

        # Begin Semantic Analysis
        self.decorate()

    ####################################################################################################################
    def decorate(self):
        print()

    def bind_symbols(self):
        print()

    ####################################################################################################################

# END: class ASTtoDAST:
########################################################################################################################