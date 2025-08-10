# main.py

from lark import Lark
from pathlib import Path
from compiler.front_end.cst_to_ast import CSTtoAST
from compiler.front_end.ast_to_dast import ASTtoDAST, DecNode

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

    ####################################################################################################################
    # Test Code
    print("\033[33;51m[Reading...]\n[Displaying Source Code]\033[0m")
    code = ("static const long long int* &&main(int* param1, char(cast_var), float param2){"
            "\n if (1 < 2 + 1 - 1 / 1)"
            "\n { int a = 10;"
            "\n }"
            "\n return 0;"
            "\n }"
            "\n")

    # code = (
    #     "int main(int argc, char param = 'x') {\n"
    #     "  int x = 1, y = {2}, z = x + y * 3;\n"
    #     "  x += y, z -= 1;\n"
    #     "  if (x < z)\n"
    #     "    x++;\n"
    #     "  else {\n"
    #     "    y = x ? y : z;\n"
    #     "  }\n"
    #     "  while (x < 10)\n"
    #     "    x = x * 2;\n"
    #     "  do z--; while (z > 0);\n"
    #     "  for (int i = 0; i < 5; i++)\n"
    #     "    x = x + i;\n"
    #     "  switch (x) {\n"
    #     "    case 1: break;\n"
    #     "    case 2: x = 3; break;\n"
    #     "    default: x = 4;\n"
    #     "  }\n"
    #     "  label1: goto label1;\n"
    #     "  return;\n"
    #     "}\n")

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

    # decorator = ASTtoDAST()
    # dast = decorator.decorate(ast)
    #
    # buffer = DecNode("test_node_A")
    # buffer.children.append(DecNode("test_node_B"))
    # dast.children.append(buffer)
    #
    # print(dast.pretty())



    ####################################################################################################################
    # Generate -> LLVM IR
    print("\033[34;51m[Generating...]\n[Displaying LLVM IR]\033[0m")



########################################################################################################################

if __name__ == '__main__':
    main()