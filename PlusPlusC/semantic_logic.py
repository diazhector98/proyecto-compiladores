from DirectorioFunciones import VariableTableRecord, VarType, FunctionDirectoryRecord
from operators import Operator
from SemanticCube import SemanticCube
from semantic_stack import SemanticStack
from quadruple import Quadruple

class SemanticHandler:
    temp_index = 0
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

    def create_temp_var(self, vtype):
        name = "temp_" + str(self.temp_index)
        self.current_var_table[name] = VariableTableRecord(
            name = name,
            type = vtype
        )
        self.temp_index = self.temp_index + 1
        return name

    def set_quadruple(self):
        print(self.stack.operands)
        if len(self.stack.operands) >= 2 and len(self.stack.operators) >= 1:
            right_operand = self.stack.operands.pop()
            left_operand = self.stack.operands.pop()
            operator = Operator(self.stack.operators.pop())
            right_operand_type = self.stack.types.pop()
            left_operand_type = self.stack.types.pop()
            cube_result = self.cube[right_operand_type][left_operand_type][operator]
            if cube_result != "err":
                temp = self.create_temp_var(cube_result)
                quadruple = Quadruple(Operator(operator), left_operand, right_operand, temp)
                self.quadruples.append(quadruple)
                self.consume_operand(temp, cube_result)
            else:
                print("type mismatch between operand", left_operand, "and", right_operand)
        else:
            print("Error: Not enough operands")
    
    
    def get_variable(self, var_name):
        var = self.current_var_table[var_name]
        if var is None:
            print("var is not declared")
        return var


    def add_var_operand(self, var_name):
        var = self.current_var_table[var_name]
        if var is None:
            print("var is not declared")
        else:
            self.consume_operand(var.name, var.type)
            self.stack.operators.append(Operator.ASSIGN)

            self.stack.operands.reverse()
            self.stack.operators.reverse()

            right_operand = self.stack.operands.pop()
            left_operand = self.stack.operands.pop()
            operator = Operator(self.stack.operators.pop())
            right_operand_type = self.stack.types.pop()
            left_operand_type = self.stack.types.pop()
            cube_result = self.cube[right_operand_type][left_operand_type][operator]
            if cube_result != "err":
                quadruple = Quadruple(Operator(operator), right_operand, None, left_operand)
                self.quadruples.append(quadruple)
                
                #print a los quadruplos actuales
                print("Cuadruplos")
                print("---------")
                for quad in self.quadruples:
                    print(quad)
            else:
                print("type mismatch")


            