# main.py

from lark import Lark
from pathlib import Path
from compiler.front_end.transformer import CSTtoAST
from compiler.front_end.decorator import ASTtoDAST
from compiler.context import CompilerContext

####################
# GlOBAL CONSTANTS #
####################

GRAMMAR_PATH     = Path(__file__).parent / "compiler" / "front_end" / "grammar.lark"
SOURCE_CODE_PATH = Path(__file__).parent / "tests" / "test_1.cpp"

########################################################################################################################
def main():

    print("\nhullo world ^w^\n")

    # INITIALIZE COMPILER CONTEXT
    context = CompilerContext()


    ########################################################################################################################

    # Load Grammar File
    with open(GRAMMAR_PATH, "r") as f:
        grammar = f.read()

    ####################################################################################################################

    # Load Source Code File
    with open(SOURCE_CODE_PATH, "r") as f:
        code = f.read()
    print(code)

    ####################################################################################################################
    # Parse -> CST
    print("\033[32;51m[Parsing...]\n[Displaying CST]\033[0m")
    parser = Lark(grammar, start="start")
    cst = parser.parse(code)
    print(cst.pretty())

    ####################################################################################################################
    # Transform -> AST

    print("\033[91;51m[Transforming...]\n[Displaying AST]\033[0m")
    transformer = CSTtoAST()
    ast = transformer.transform(cst)
    print(ast.pretty())

    ####################################################################################################################
    # Decorate -> D-AST

    print("\033[35;51m[Decorating...]\n[Displaying Decorated-AST] \033[0m")
    decorator = ASTtoDAST(ast, context)
    decorator.mutate()
    print(ast.pretty())



    ####################################################################################################################
    # Generate -> LLVM IR
    print("\033[34;51m[Generating...]\n[Displaying LLVM IR]\033[0m")



########################################################################################################################

if __name__ == '__main__':
    main()