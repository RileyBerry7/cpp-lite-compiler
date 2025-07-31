# main.py

from lark import Lark
from pathlib import Path
from compiler.front_end.cst_to_ast import CSTtoAST
from compiler.front_end.ast_to_dast import ASTtoDAST

####################
# GlOBAL CONSTANTS #
####################

GRAMMAR_PATH = Path(__file__).parent / "compiler" / "front_end" / "grammar.lark"

########################################################################################################################
def main():

    print("\nhullo world ^w^\n")

    # Load Grammar
    with open(GRAMMAR_PATH, "r") as f:
        grammar = f.read()

    # Test Code
    code = "int main(char param1) {return 0;}"

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
    print('\n')
    decorator = ASTtoDAST()
    dast = decorator.decorate(ast)

    ####################################################################################################################
    # Generate -> LLVM IR
    print("\033[34;51m[Generating...]\n[Displaying LLVM IR]\033[0m")
    print(dast.pretty())

########################################################################################################################

if __name__ == '__main__':
    main()