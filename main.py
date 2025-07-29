# main.py
from lark import Lark
from pathlib import Path

from compiler.front_end import cst_to_ast

GRAMMAR_PATH = Path(__file__).parent / "compiler" / "front_end" / "grammar.lark"

def main():

    print("hullo ^w^\n")

    # Load Grammar
    with open(GRAMMAR_PATH, "r") as f:
        grammar = f.read()

    # Create Parser
    parser = Lark(grammar, start="start")

    # Create CST with Test Code
    code = "int main(int var1, char var2) {return 0;}"
    tree = parser.parse(code)
    print(tree.pretty())




if __name__ == '__main__':
    main()