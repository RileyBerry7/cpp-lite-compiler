# main.py
from lark import Lark
from pathlib import Path

from compiler.front_end.cst_to_ast import CSTtoAST

GRAMMAR_PATH = Path(__file__).parent / "compiler" / "front_end" / "grammar.lark"

def main():

    print("hullo ^w^\n")

    # Load Grammar
    with open(GRAMMAR_PATH, "r") as f:
        grammar = f.read()

    # Test Code
    code = "int main(char param1) {return 0;}"

    # Create CST with Test Code
    print("\033[32m[Parsing...]\n[Displaying CST]\033[0m")
    parser = Lark(grammar, start="start")
    cst = parser.parse(code)
    print(cst.pretty())

    print("\033[91m[Transforming...]\n[Displaying AST]\033[0m")
    transformer = CSTtoAST()
    ast = transformer.transform(cst)
    print(ast.pretty())




if __name__ == '__main__':
    main()