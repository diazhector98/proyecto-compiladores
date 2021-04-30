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
    jumps_stack = []

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

    def consume_operand(self, operand, var_type=None):
        if var_type == None:
            try:
                t = self.current_var_table[operand]
                self.stack.push_operand(t.name, t.type)
            except KeyError:
                print("varibale", operand, "does not exist")
        else:
            self.stack.push_operand(operand, var_type)

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
            else:
                print("type mismatch between operand", left_operand, left_operand_type,  "and", right_operand, right_operand_type)

    def set_initial_if(self):
        self.set_conditional_block()

    def set_initial_while(self):
        # Jump index para regresar a evaluar la condicion del while (al cuádruplo de la condición)
        jump_index = len(self.quadruples) - 1
        self.jumps_stack.append(jump_index)
        self.set_conditional_block()

    def set_conditional_block(self):
        if self.stack.operands:
            result = self.stack.operands.pop()
            if self.stack.types.pop() == VarType.BOOL:
                quadruple = Quadruple(Operator.GOTOF, result, None, None)
                self.quadruples.append(quadruple)
                jump_index = len(self.quadruples) - 1
                self.jumps_stack.append(jump_index)
            else:
                raise TypeError("Error: Type of operation must be of type BOOL")
        else:
            raise Exception("Error: Not enough operands")

    def set_end_of_if(self):
        if self.jumps_stack:
            quadruple_index_to_set = self.jumps_stack.pop()
            final_jump_index = len(self.quadruples) + 1
            self.set_final_jump(quadruple_index_to_set, final_jump_index)
        else:
            raise Exception("Error: Jump stack is empty")

    def set_end_of_while(self):
        end_jump_index = self.jumps_stack.pop()
        condition_jump_index = self.jumps_stack.pop()
        quadruple = Quadruple(Operator.GOTO, None, None, condition_jump_index)
        self.quadruples.append(quadruple)        
        self.set_final_jump(end_jump_index, len(self.quadruples))

    def set_final_jump(self, quadruple_index_to_set, final_jump_index):
        self.quadruples[quadruple_index_to_set].temp_result = final_jump_index

    def set_else(self):
        quadruple = Quadruple(Operator.GOTO, None, None, None)
        self.quadruples.append(quadruple)

        if self.jumps_stack:
            quadruple_index_to_set = self.jumps_stack.pop()
            self.jumps_stack.append(len(self.quadruples) - 1)
            self.set_final_jump(quadruple_index_to_set, len(self.quadruples) + 1)
        else:
            raise Exception("Jump stack error")

    # Método de debugging
    def print_quadruples(self):
        for index, quad in enumerate(self.quadruples):
            print(f"{index})", quad.operator, quad.temp_result)

       