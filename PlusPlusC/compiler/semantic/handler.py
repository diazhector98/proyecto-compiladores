from compiler.semantic.common.DirectorioFunciones import VariableTableRecord, VarType, FunctionDirectoryRecord
from compiler.semantic.common.operators import Operator
from compiler.semantic.cube.cube import SemanticCube
from compiler.semantic.stack import SemanticStack
from compiler.semantic.common.quadruple import Quadruple
from compiler.semantic.memory.virtual_memory import VirtualMemory

class SemanticHandler:
    temp_index = 0
    global_var_table = dict()   
    current_var_table = dict()
    constants_table = dict()
    functions_directory = dict()
    quadruples: [Quadruple] = []
    jumps_stack = []
    current_function = None

    def __init__(self):
        self.cube = SemanticCube()
        self.stack = SemanticStack()
        self.memory = VirtualMemory()

    def initialize_program(self):
        goto_main = Quadruple(Operator.GOTO, None, None, None)
        self.quadruples.append(goto_main)
        self.jumps_stack.append(0)

    def set_goto_main(self):
        main_jump = self.jumps_stack.pop()
        self.set_final_jump(main_jump, len(self.quadruples))

    def set_init_func(self, func_name, t):
        self.functions_directory[func_name] = FunctionDirectoryRecord(
            name = func_name,
            return_type= t,
            address = len(self.quadruples)
        )
        self.current_function = func_name

    def set_parametros(self, parametros):
        for (param_name, param_var_type) in parametros:
            self.functions_directory[self.current_function].add_param((param_name, param_var_type))
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

    def consume_operand(self, operand, var_type=None, is_constant=False):
        if is_constant:
            self.consume_constant_operand(operand, var_type)
        else:
            self.consume_var_operand(operand)

    def consume_var_operand(self, operand):
        try:
            t = self.current_var_table[operand]
            self.stack.push_operand(t.name, t.type)
        except KeyError:
            print("variable", operand, "does not exist")

    def consume_constant_operand(self, constant, var_type):
        constant_address = self.constants_table.get(constant)
        if not constant_address:
            constant_address = self.memory.create_constant_address(var_type)
        self.stack.push_operand(constant_address, var_type)

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

    def set_function_call(self, func_name, arguments):
        function = self.functions_directory[func_name]
        function_params_types = []
        arguments_types = []

        #Revisar funcion en el directorio de funciones
        if function is None:
            print("Funcion no se encuentra en directorio de funciones")
        else:
            #Revisar numero de parametros
            if len(arguments) != len(function.params):
                print("El numero de parametros que la funcion:", function.name, "requiere es incorrecta.")
            else:
                #Revisar el tipo de parametros
                for param in (function.params):
                    function_params_types.append(param[1])

                for argument in arguments:
                    arguments_types.append(argument[1])
                    
                if function_params_types != arguments_types:
                    print("El tipo de parametros que la función espera es incorrecto.")
                else:
                    #Si todas las restricciones se cumplen
                    quadruple = Quadruple(Operator.ERA, None, None, func_name)
                    self.quadruples.append(quadruple)
        
                    arguments.reverse()
                    for index, (argument, argument_type) in enumerate(arguments):
                        param_quad = Quadruple(Operator.PARAMETER, argument, None, f"p{index}")
                        self.quadruples.append(param_quad)

                    gosub_quad = Quadruple(Operator.GOSUB, None, None, func_name)
                    self.quadruples.append(gosub_quad)
                    
                    function_params_types.clear()
                    arguments_types.clear()
                    
    def handle_return(self):
        function = self.functions_directory[self.current_function]
        operand = self.stack.operands.pop()
        operand_type = self.stack.types.pop()

        if function.return_type.name == operand_type.name:
            quad = Quadruple(Operator.RETURN, None, None, operand)
            self.quadruples.append(quad)
        else:
            print("El tipo de retorno que la función espera es incorrecto.")
        
    # Método de debugging
    def print_quadruples(self):
        for index, quad in enumerate(self.quadruples):
            operator = quad.operator
            left_operand = quad.left_operand
            right_operand = quad.right_operand
            result = quad.temp_result
            print ("{:<12} {:<10} {:<10} {:<10}".format(operator.name, str(left_operand), str(right_operand), str(result)))

    def end_func(self):
        function = self.functions_directory[self.current_function]
        if function is None:
            print("Funcion no se encuentra en directorio de funciones")
        else:
            quadruple = Quadruple(Operator.ENDFUNC, None, None, None)
            self.quadruples.append(quadruple)