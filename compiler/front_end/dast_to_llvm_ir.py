# dast_to_llvm_ir.py

from ast_to_dast import DecNode
from llvmlite import ir


########################################################################################################################
class IRGenerator:
    def __init__(self):

        # Current Context
        self.symbol_table  = [{}]
        self.error_list    = []

        # Current Scope
        self.module:   Any = None
        self.function: Any = None # most recently created function

    ####################################################################################################################
    def generate_llvm_ir(self, decorated_ast: DecNode)
        """
        Starts the LLVM IR generation process. Uses recursively called IR generating methods to traverse the decorated 
        AST using depth-first search (DFS), and emits the corresponding LLVM IR code as it goes.z
        """

        # Create: IR Module
        if decorated_ast.name = "program":
            self.emit_module(decorated_ast)

        # Error: D-AST Root Not Found
        else:
            print("\033[32;51mError: Root Not Found.\033[0m")

    ####################################################################################################################
    def emit_module(self, curr_node: DecNode):

        # Create: IR Module (LLVM IR top-most container)
        self.module = ir.Module(name="module")

       # Loop through all children of the root node, and emit their IR representations
        for child in curr_node.children:

            # If: Function Definition Node
            if child.name == "func_def":
                # Create: Function
                self.emit_function(child)

    ####################################################################################################################
    def emit_function_type(self, func_def_node: DecNode):

        # Retrieve: Return Type
        if "return_type" in func_def_node.decorations:
            return_type = self.resolve_type(func_def_node.decorations["return_type"])

        # Error: Return Type Not Found
        else:
            self.report_error(expected="return_type", found=func_def_node.children[0].name)
            return_type = None

        # Retrieve: Parameter Types
        if "param_types" in func_def_node.decorations:
            parameter_types = [self.resolve_type(param) for param in func_def_node.decorations["param_types"]]
        # Else: No Parameters
        else:
            parameter_types = []

        # Return LLVM IR Function Type Object
        return ir.FunctionType(return_type, parameter_types)

    ####################################################################################################################
    def emit_function(self, curr_node: DecNode):
        # Create Function Type
        function_type = self.emit_function_type(curr_node)

        # Retrieve: Function Name
        if "func_name" in curr_node.decorations:
            function_name = curr_node.decorations["func_name"]

        # Error: Function Name Not Found
        else:
            self.report_error(expected="function_name", found=curr_node.children[0].name)
            function_name = "unknown_function"

        # Create Function in Module
        self.function = ir.Function(self.module, function_type, function_name)

    ####################################################################################################################
    def emit_builder(self, curr_node: DecNode):
        print()

    ####################################################################################################################
    def emit_block(self, curr_node: DecNode):
        print()

    ####################################################################################################################
    def report_error(self, expected: str, found: str = None):
        self.error_list.append("\033[32;51mError:\tExpected: " + expected + "\tFound: " + found + "\033[0m")

   ####################################################################################################################
    def resolve_type(self, type_name: str):
        """
        Resolve the type name to an LLVM IR type.
        """
        if type_name == "int":
            return ir.IntType(32)
        elif type_name == "float":
            return ir.FloatType()
        elif type_name == "double":
            return ir.DoubleType()
        elif type_name == "char":
            return ir.IntType(8)
        else:
            # self.report_error(expected="valid type", found=type_name)
            return None

# END - class IntermediateCodeGenerator:
####################################################################################################################