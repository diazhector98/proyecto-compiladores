from compiler.semantic.common.DirectorioFunciones import VariableTableRecord, VarType, FuncReturnType, FunctionDirectoryRecord
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

    def add_global(self, var_name, var_type):
        address = self.memory.create_global_address(var_type)
        self.global_var_table[var_name] = VariableTableRecord(
            name = var_name,
            type = var_type,
            address = address
        )

    def set_init_func(self, func_name, t):
        self.functions_directory[func_name] = FunctionDirectoryRecord(
            name = func_name,
            return_type= t,
            address = len(self.quadruples)
        )
        self.current_function = func_name

    def set_parametros(self, parametros):
        parametros.reverse()
        for (param_name, param_var_type) in parametros:
            address = self.memory.create_local_address(param_var_type)
            self.functions_directory[self.current_function].add_param((param_name, param_var_type, address))
            self.current_var_table[param_name] = VariableTableRecord(
                name = param_name,
                type = param_var_type,
                address = address
                )

    def set_variable(self, var_name, var_type, rows=1, columns=1):
        address = self.memory.create_local_address(var_type, size=(rows * columns))
        self.current_var_table[var_name] = VariableTableRecord(
            name = var_name,
            type = var_type,
            address = address,
            dimensions = (rows, columns)
            )
        self.create_constant(rows, VarType.INT)
        self.create_constant(columns, VarType.INT)

    def create_constant(self, value, type):
        constant_address = self.constants_table.get(value)
        if not constant_address:
            constant_address = self.memory.create_constant_address(type)
            self.constants_table[value] = constant_address
    
    def get_constant(self, value):
        constant_address = self.constants_table.get(value)
        if constant_address != None:
            return constant_address
        else:
            print("Constant variable is not registered yet.")

    def consume_operator(self, operator):
        self.stack.push_operator(operator)

    def consume_operand(self, operand, var_type=None, is_constant=False, index=None):
        # Index para arreglos y matrices
        if is_constant:
            self.consume_constant_operand(operand, var_type)
        else:
            self.consume_var_operand(operand, index=index)

    def consume_var_operand(self, operand, index=None):
        if index != None:
            # Hacer algo para los arreglos
            pass
        try:
            var = self.var_lookup(operand)
            # TODO: En el futuro, todas deberían tener direcciones
            if var.address:
                self.stack.push_operand(var.address, var.type)
            else:
                self.stack.push_operand(var.name, var.type)
        except Exception:
            print("variable", operand, "does not exist")

    def consume_array_usage(self, array_name, index_operand):
        var = self.var_lookup(array_name)
        if var is None:
            raise Exception("Array does not exist")
        
        base_address = var.address
        index_address = index_operand[0]
        index_type = index_operand[1]
        # Verificar que el indice este en rango
        rows_address = self.constants_table.get(var.dimensions[0])
        verify_quadruple = Quadruple(Operator.VERIFY, index_address, None, rows_address)
        self.quadruples.append(verify_quadruple)

        constant_address = self.get_constant(base_address)
        pointer_to_temp_address = self.memory.create_pointer_address(var.type)
        add_array_base_quadruple = Quadruple(Operator.SUM, index_address, constant_address, pointer_to_temp_address)
        self.quadruples.append(add_array_base_quadruple)

        self.stack.push_operand(pointer_to_temp_address, var.type)


    # Buscar variable en tabla de variables locales y globales
    def var_lookup(self, var_name):
        var = self.current_var_table.get(var_name)
        if var:
            return var
        var = self.global_var_table[var_name]
        return var

    def consume_constant_operand(self, constant, var_type):
        constant_address = self.constants_table.get(constant)
        if not constant_address:
            constant_address = self.memory.create_constant_address(var_type)
            self.constants_table[constant] = constant_address
        self.stack.push_operand(constant_address, var_type)

    # Por lo pronto, solo guardamos el cuadruplo con el nombre de la variable
    def handle_read(self, id):
        var = self.var_lookup(id)
        quadruple = Quadruple(Operator.READ, None, None, var.address)
        self.quadruples.append(quadruple)

    def handle_print(self):
        if self.stack.operands:
            var_name = self.stack.operands.pop()
            quadruple = Quadruple(Operator.PRINT, None, None, var_name)
            self.quadruples.append(quadruple)

    def create_temp_var(self, vtype):
        name = "temp_" + str(self.temp_index)
        address = self.memory.create_temporal_address(vtype)
        self.current_var_table[name] = VariableTableRecord(
            name = name,
            type = vtype,
            address = address
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
                temp_address = self.current_var_table[temp].address
                temp_type = self.current_var_table[temp].type

                #set el count de temporales dependiendo el tipo
                if temp_type == VarType.INT:
                    self.functions_directory[self.current_function].temp_var_int_size += 1
                elif temp_type == VarType.FLOAT:
                    self.functions_directory[self.current_function].temp_var_float_size += 1
                elif temp_type == VarType.CHAR:
                    self.functions_directory[self.current_function].temp_var_char_size += 1
                elif temp_type == VarType.BOOL:
                    self.functions_directory[self.current_function].temp_var_bool_size += 1

                quadruple = Quadruple(Operator(operator), left_operand, right_operand, temp_address)
                self.quadruples.append(quadruple)
                self.consume_operand(temp, cube_result)
            else:
                print("Setting Quadruple: type mismatch between operand", left_operand, "and", right_operand)
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
            self.stack.types.reverse()

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
                print("Adding var operand: type mismatch between operand", left_operand, left_operand_type,  "and", right_operand, right_operand_type)

    def handle_array_assign(self, var_name):
        var = self.current_var_table[var_name]
        if var is None:
            print("var is not declared")
        else:
            self.consume_operand(var.name, var.type)
            self.stack.operators.append(Operator.ASSIGN)

            self.stack.operands.reverse()
            self.stack.operators.reverse()
            self.stack.types.reverse()

            array_index_operand = self.stack.operands.pop()
            right_operand = self.stack.operands.pop()
            array_base_address = self.stack.operands.pop()


            array_index_type = self.stack.types.pop()
            right_operand_type = self.stack.types.pop()
            array_type = self.stack.types.pop()

            # Agregando direccion base a tabla de constantes
            self.create_constant(array_base_address, array_type)

            operator = Operator(self.stack.operators.pop())
            cube_result = self.cube[right_operand_type][array_type][operator]

            # Validando que array_index_type sea int
            if array_index_type == VarType.INT:
                if cube_result != "err":
                    # Agregando Verify
                    rows_address = self.constants_table.get(var.dimensions[0])
                    verify_quadruple = Quadruple(Operator.VERIFY, array_index_operand, None, rows_address)
                    self.quadruples.append(verify_quadruple)

                    # Haciendo suma de direccion base
                    constant_address = self.get_constant(array_base_address)
                    pointer_to_temp_address = self.memory.create_pointer_address(array_type)
                    add_array_base_quadruple = Quadruple(Operator.SUM, array_index_operand, constant_address, pointer_to_temp_address)
                    self.quadruples.append(add_array_base_quadruple)

                    # Guardando direccion de temporal en direeccion de pointer
                    assign_right_operand_to_pointer_quadruple = Quadruple(Operator.ASSIGN, right_operand, None, pointer_to_temp_address)
                    self.quadruples.append(assign_right_operand_to_pointer_quadruple)
                else:
                    print("type mismatch between operand", array_base_address, array_type,  "and", right_operand, right_operand_type)
            else:
                print("Error: the array index type must be an integer.")

    def handle_matrix_assign(self, var_name):
        var = self.current_var_table[var_name]
        if var is None:
            print("var is not declared")
        else:
            self.consume_operand(var.name, var.type)
            self.stack.operators.append(Operator.ASSIGN)

            self.stack.operands.reverse()
            self.stack.operators.reverse()
            self.stack.types.reverse()

            matrix_first_index_operand = self.stack.operands.pop()
            matrix_second_index_operand = self.stack.operands.pop()
            right_operand = self.stack.operands.pop()
            matrix_base_address = self.stack.operands.pop()

            matrix_first_index_type = self.stack.types.pop()
            matrix_second_index_type = self.stack.types.pop()
            right_operand_type = self.stack.types.pop()
            matrix_type = self.stack.types.pop()

            # Agregando direccion base a tabla de constantes
            self.create_constant(matrix_base_address, matrix_type)
            operator = Operator(self.stack.operators.pop())
            cube_result = self.cube[right_operand_type][matrix_type][operator]

            if matrix_first_index_type == VarType.INT and matrix_second_index_type == VarType.INT:
                
                if cube_result != "err":
                    
                    # Agregando Verify de la primera dimension
                    rows_address = self.constants_table.get(var.dimensions[0])
                    verify_quadruple = Quadruple(Operator.VERIFY, matrix_first_index_operand, None, rows_address)
                    self.quadruples.append(verify_quadruple)

                    # Agregando Multiply s1*m1
                    m_one = int(((var.dimensions[0] + 1) * (var.dimensions[1] + 1)) / (var.dimensions[0] + 1))
                    m_one_constant = self.create_constant(m_one, VarType.INT)
                    m_one_constant_adress = self.get_constant(matrix_base_address)
                    temp_multiply = self.create_temp_var(VarType.INT)
                    temp_multiply_address = self.current_var_table[temp_multiply].address
                    multiply_m_one_quadruple = Quadruple(Operator.MULTIPLY, matrix_first_index_operand, m_one_constant_adress, temp_multiply_address)
                    self.quadruples.append(multiply_m_one_quadruple)

                    # Agregando Verify de la segunda dimension s2
                    columns_address = self.constants_table.get(var.dimensions[1])
                    verify_quadruple = Quadruple(Operator.VERIFY, matrix_second_index_operand, None, columns_address)
                    self.quadruples.append(verify_quadruple)
                    
                    # Sumando s1*m1 + s2
                    temp_sum = self.create_temp_var(VarType.INT)
                    temp_sum_address = self.current_var_table[temp_sum].address
                    sum_quadruple = Quadruple(Operator.SUM, temp_multiply_address, matrix_second_index_operand, temp_sum_address)
                    self.quadruples.append(sum_quadruple)

                    # Haciendo suma de direccion base s1*m1 + s2 + dirBase
                    matrix_constant_address = self.get_constant(matrix_base_address)
                    pointer_to_temp_address = self.memory.create_pointer_address(matrix_type)
                    add_matrix_base_quadruple = Quadruple(Operator.SUM, temp_sum_address, matrix_constant_address, pointer_to_temp_address)
                    self.quadruples.append(add_matrix_base_quadruple)

                    # Guardando direccion de temporal en direeccion de pointer
                    assign_right_operand_to_pointer_quadruple = Quadruple(Operator.ASSIGN, right_operand, None, pointer_to_temp_address)
                    self.quadruples.append(assign_right_operand_to_pointer_quadruple)
                else:
                    print("type mismatch between operand", matrix_base_address, matrix_type,  "and", right_operand, right_operand_type)
            else:
                print("Error: both matrix indices types must be integers.")


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
                print("set_conditional_block", "jump:", jump_index)
            else:
                raise TypeError("Error: Type of operation must be of type BOOL")
        else:
            raise Exception("Error: Not enough operands")

    def set_end_of_if(self):
        if self.jumps_stack:
            quadruple_index_to_set = self.jumps_stack.pop()
            final_jump_index = len(self.quadruples)
            print("end of if", "jump:", final_jump_index)
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
            print("set_else", "jump:", len(self.quadruples) + 1)
            self.set_final_jump(quadruple_index_to_set, len(self.quadruples))
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
                        param_address = function.params[index][2]
                        param_quad = Quadruple(Operator.PARAMETER, argument, None, param_address)
                        self.quadruples.append(param_quad)

                    gosub_quad = Quadruple(Operator.GOSUB, None, None, func_name)
                    self.quadruples.append(gosub_quad)
                    
                    #Si el tipo de retorno de la funcion no es void,
                    #guardar temp en direccion de funcion
                    if function.return_type != FuncReturnType.VOID:

                        if function.return_type == FuncReturnType.INT:
                            temp = self.create_temp_var(VarType.INT)
                            self.functions_directory[self.current_function].temp_var_int_size += 1

                        if function.return_type == FuncReturnType.FLOAT:
                            temp = self.create_temp_var(VarType.FLOAT)
                            self.functions_directory[self.current_function].temp_var_float_size += 1

                        if function.return_type == FuncReturnType.CHAR:
                            temp = self.create_temp_var(VarType.CHAR)
                            self.functions_directory[self.current_function].temp_var_char_size += 1

                        if function.return_type == FuncReturnType.BOOL:
                            temp = self.create_temp_var(VarType.BOOL)
                            self.functions_directory[self.current_function].temp_var_bool_size += 1

                        temp_address = self.current_var_table[temp].address
                        temp_type = self.current_var_table[temp].type

                        #Obtener address global de func de la tabla de vars globales
                        function_address = self.global_var_table[function.name].address

                        quadruple = Quadruple(Operator.ASSIGN, function_address, None, temp_address)
                        self.quadruples.append(quadruple)
                        self.consume_operand(temp, temp_type)

                    #Reset a listas para comparar de nuevo parametros 
                    #de funcion con los parametros que se mandaron con la func a llamar
                    function_params_types.clear()
                    arguments_types.clear()
                    
    def handle_return(self):
        function = self.functions_directory[self.current_function]
        operand = self.stack.operands.pop()
        operand_type = self.stack.types.pop()

        if function.return_type.name == operand_type.name:
            function_global_address = self.global_var_table[function.name].address
            quad = Quadruple(Operator.RETURN, operand, None, function_global_address)
            self.quadruples.append(quad)
        else:
            raise Exception("El tipo de retorno que la función espera es incorrecto.")
        
    # Método de debugging
    def print_quadruples(self):
        for index, quad in enumerate(self.quadruples):
            print(index, str(quad))

    def print_constants_table(self):
        for key in self.constants_table:
            address = self.constants_table[key]
            print ("{:<7} {:<12}".format(address, key))

    def print_globals_table(self):
        for key in self.global_var_table:
            address = self.global_var_table[key].address
            print ("{:<7} {:<12}".format(address, key))

    def end_func(self):
        function = self.functions_directory[self.current_function]
        if function is None:
            raise Exception("Funcion no se encuentra en directorio de funciones")
        quadruple = Quadruple(Operator.ENDFUNC, None, None, None)
        self.quadruples.append(quadruple)
        for var_name in self.current_var_table:
            local_type = self.current_var_table[var_name].type
            #set el count de locales dependiendo el tipo
            if local_type == VarType.INT:
                self.functions_directory[self.current_function].local_var_int_size += 1
            elif local_type == VarType.FLOAT:
                self.functions_directory[self.current_function].local_var_float_size += 1
            elif local_type == VarType.CHAR:
                self.functions_directory[self.current_function].local_var_char_size += 1
            elif local_type == VarType.BOOL:
                self.functions_directory[self.current_function].local_var_bool_size += 1
        self.memory.reset_local_and_temp_memory()