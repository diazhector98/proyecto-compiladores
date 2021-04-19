from DirectorioFunciones import VariableTableRecord, VarType, FunctionDirectoryRecord
from SemanticCube import SemanticCube
from SemanticCubeRules import Operator
from semantic_stack import SemanticStack

class SemanticHandler:
    
    global_var_table = dict()   
    current_var_table = dict()
    functions_directory = dict()

    def __init__(self):
        self.cube = SemanticCube()
        self.stack = SemanticStack()

    def set_init_func(self, func_name, t):
        self.functions_directory[func_name] = FunctionDirectoryRecord(
            name = func_name,
            return_type= t
        )

    def set_parametros(self, parametros):
        for (param_name, param_var_type) in parametros:
            self.current_var_table[param_name] = VariableTableRecord(
                name = param_name,
                type = param_var_type
                )

    def set_variable(self, var_name, var_type):
        self.current_var_table[var_name] = VariableTableRecord(
            name = var_name,
            type = var_type
            )
    
    def consume_operator(self, operator):
        self.stack.push_operator(operator)