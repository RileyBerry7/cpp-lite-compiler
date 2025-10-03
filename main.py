# main.py

from lark import Lark
from pathlib import Path
from compiler.front_end.transformer import CSTtoAST
from compiler.front_end.decorator import ASTtoDAST
from compiler.front_end.llvm_generator import LLVMGenerator
from compiler.context import CompilerContext
from compiler.utils.colors import colors
from llvmlite import binding as llvm
import ctypes

####################
# GlOBAL CONSTANTS #
####################

GRAMMAR_PATH      = Path(__file__).parent / "compiler" / "front_end" / "grammar.lark"
SOURCE_CODE_PATH  = Path(__file__).parent / "tests" / "test_3.cpp"
INCLUDE_FILE_PATH = Path(__file__).parent / "include"
OUTPUT_PATH       = Path(__file__).parent / "output"


import subprocess
def preprocess_source(source: str) -> str:
    try:
        result = subprocess.run(
            ["clang", "-E", "-P", "-I", str(INCLUDE_FILE_PATH), "-"],
            input=source,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("=== clang STDOUT ===")
        print(e.stdout)
        print("=== clang STDERR ===")
        print(e.stderr)
        raise

########################################################################################################################
def main():

    print("\nhullo world ^w^\n")

    # INITIALIZE COMPILER CONTEXT
    context = CompilerContext()


    ########################################################################################################################

    # Load Grammar File
    with open(GRAMMAR_PATH, "r", encoding="utf-8", errors="replace") as f:
        grammar = f.read()

    ####################################################################################################################
    print(colors.cyan.boxed("Path: "+ str(SOURCE_CODE_PATH) +"\n[Printing Source Code]"))
    # Load Source Code File
    with open(SOURCE_CODE_PATH, "r") as f:
        code = f.read()
    code = preprocess_source(code)
    print(code)    #
    ####################################################################################################################
    # Parse -> CST
    print(colors.green.boxed("[Parsing...]\n[Displaying CST]"))
    print("\n...\n")
    # parser = Lark(grammar, start='start', parser='lalr', lexer='contextual', debug=True, strict=True)
    parser = Lark(grammar, start="start", parser="earley", ambiguity="explicit")
    cst = parser.parse(code)
    # print(cst.pretty())

    ####################################################################################################################
    # Transform -> AST

    print(colors.red.boxed("[Transforming...]\n[Displaying AST]"))
    transformer = CSTtoAST()
    cst = transformer.disambiguate(cst)
    ast = transformer.transform(cst)
    print(ast.pretty())

    ####################################################################################################################
    # Decorate -> D-AST

    print(colors.pink.boxed("[Decorating...]\n[Displaying Decorated-AST]"))
    print("\n...\n")
    # decorator = ASTtoDAST(ast, context)
    # decorator.decorate()
    # print(ast.pretty())



    ####################################################################################################################
    # Generate -> LLVM IR
    print(colors.blue.boxed("[Generating...]\n[Displaying LLVM IR]"))
    ir_generator = LLVMGenerator(ast, context)
    ir_generator.generate()
    llvm_ir = ir_generator.module
    print(llvm_ir)

    ####################################################################################################################
    # ASSEMBLE & LINK WITH CLANG

    ####################################################################################################################
    # LLVM JIT EXECUTION

    # print( colors.yellow.boxed("[Interpreting]\n[Executing With MCJIT Engine\n"))

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    llvm_ir = str(llvm_ir)   # your IR string

    # Parse IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()

    # Create engine
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    engine.add_module(mod)
    engine.finalize_object()

    # Run main
    func_ptr = engine.get_function_address("main")
    cfunc = ctypes.CFUNCTYPE(ctypes.c_int)(func_ptr)
    res = cfunc()
    print("main returned:", res)

    # print("\n\n\n")

########################################################################################################################

if __name__ == '__main__':
    main()

    from compiler.utils.colors import colors
    print()
    print( colors.yellow.boxed("[Interpreting]\n[Executing With MCJIT Engine\n"))