from DirectorioFunciones import VariableTableRecord, VarType, FunctionDirectoryRecord
from operators import Operator
from SemanticCube import SemanticCube
from semantic_stack import SemanticStack
from quadruple import Quadruple

class SemanticHandler:
    
    global_var_table = dict()   
    current_var_table = dict()
    functions_directory = dict()
    quadruples = []

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
    

    def consume_operand(self, operand, type):
        self.stack.push_operand(operand, type)

    # Por lo pronto, solo guardamos el cuadruplo con el nombre de la variable
    def handle_read(self, id):
        var = current_var_table[id]
        quadruple = Quadruple(Operator.READ, None, None, var.name)
        self.quadruples.append(quadruple)

    def handle_print(self):
        if self.stack.operands:
            var_name = self.stack.operands.pop()
            quadruple = Quadruple(Operator.PRINT, None, None, var_name)
            self.quadruples.append(quadruple)

            