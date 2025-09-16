# llvm_generator.py

from llvmlite import ir
from compiler.context import CompilerContext
from compiler.front_end.abstract_nodes.ast_node import ASTNode

########################################################################################################################
class LLVMGenerator:
    def __init__(self, dast_root: ASTNode, context: CompilerContext):

        self.context  = context  # Compiler context
        self.dast = dast_root    # DAST root
        self.module : ir.Module    | None = None # IR root

    ####################################################################################################################
    def generate(self):
        """ Starts the LLVM IR generation process. it goes."""
        lowering_pass = LoweringPass(self.dast, self.context, self.module)
        lowering_pass.walk()
        self.module = lowering_pass.module



####################################################################################################################
from compiler.front_end.decorator import Decorator

###################
#  LOWERING PASS  #
###################
class LoweringPass(Decorator):
    def __init__(self, root: ASTNode, context: CompilerContext, ir_root: ir.Module):
        super().__init__(root_node=root, context=context, traversal_order="both")

        self.module : ir.Module = ir_root        # IR root
        self.builder: ir.IRBuilder | None = None # Current IR builder

    ####################################################################################################################
    #  VISITOR METHODS  #
    #####################

    def translation_unit_pre(self, node: ASTNode, children: list[ASTNode]):
        self.emit_module(node)

    # def translation_unit_post(self, node: ASTNode, children: list[ASTNode]):


    ####################################################################################################################
    #  EMIT METHODS  #
    ##################

    def emit_module(self, curr_node: ASTNode):
        if self.module is not None:
            print("Error: more than one translation unit found.") # Error
        else:
            self.module = ir.Module(name=curr_node.name)  # Create: IR Module

    ####################################################################################################################
    def emit_function_type(self, func_def_node: ASTNode):
        print()

    ####################################################################################################################
    def emit_function(self, curr_node: ASTNode):
        # Create / Emit IR Constructs
        return_type = ir.DoubleType()
        arguments = (ir.DoubleType(), ir.DoubleType())
        is_variadic = False  # Can accept more more arguments than specified
        function_type = ir.FunctionType(return_type, arguments, is_variadic)
        function_name = curr_node.decorations["main"]
        function = ir.Function(self.module, function_type, function_name)

        # Allow Builder to 'Enter' New Block
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)  # update builder

        # a, b = function.args                    # parameters_and_qualifiers
        # result = builder.fadd(a, b, name="res") # emit_expression
        # self.builder.ret(result)                # return_statement
########################################################################################################################


