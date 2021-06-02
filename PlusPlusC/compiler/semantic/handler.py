from compiler.semantic.common.DirectorioFunciones import VariableTableRecord, VarType, FuncReturnType, FunctionDirectoryRecord
from compiler.semantic.common.operators import Operator
from compiler.semantic.cube.cube import SemanticCube
from compiler.semantic.stack import SemanticStack
from compiler.semantic.common.quadruple import Quadruple
from compiler.semantic.memory.virtual_memory import VirtualMemory

"""
Clase para manejar los puntos neurálgicos en las acciones semánticas.
    temp_index: guarda el índice del temporal a utilizar en una funcion
    global_var_table = guarda las variables globales 
    current_var_table = guarda las variables de una funcion
    constants_table = guarda las variables constantes de una funcion
    functions_directory = guarda las funciones utilizadas en el programa
    quadruples: guarda la lista de cuadruplos generados
    jumps_stack = pila de saltos 
    current_function = guarda la funcion en la que se encuentra el compilador
    durante el proceso de compilaciónn,
"""
class SemanticHandler:
    temp_index = 0
    global_var_table = dict()   
    current_var_table = dict()
    constants_table = dict()
    quadruples: [Quadruple] = []
    jumps_stack = []
    current_function = None

    def __init__(self):
        self.cube = SemanticCube()
        self.stack = SemanticStack()
        self.memory = VirtualMemory()
        self.functions_directory = dict()

    def initialize_program(self):
        """
            Función que inicializa la lista de cuadruplos y la pila de saltos
            y agrega la funcion global al directorio de funciones
        """
        goto_main = Quadruple(Operator.GOTO, None, None, None)
        self.quadruples = [goto_main]
        self.jumps_stack = [0]
        global_function_name = 'global'
        self.functions_directory[global_function_name] = FunctionDirectoryRecord(
            name = global_function_name,
            return_type=None,
            address = 0
        )
        self.current_function = global_function_name

    def set_init_main(self):
        """
            Función que rellena el GOTO del cuadruplo main y agrega
            la funcion main al directorio de funciones
        """
        main_jump = self.jumps_stack.pop()
        self.set_final_jump(main_jump, len(self.quadruples))
        main_function_name = 'main'
        self.functions_directory[main_function_name] = FunctionDirectoryRecord(
            name = main_function_name,
            return_type=None,
            address = len(self.quadruples)
        )
        self.current_function = main_function_name

    def add_global(self, var_name, var_type):
        """
            Función que agrega una variable global a la tabla de
            variables globales
            param var_name: nombre de la variable global
            param var_type: tipo de la variable global
        """
        address = self.memory.create_global_address(var_type)
        self.global_var_table[var_name] = VariableTableRecord(
            name = var_name,
            type = var_type,
            address = address
        )
        self.add_function_local_var_size(var_type, 1, 'global')

    def set_init_func(self, func_name, t):
        """
            Función que agrega una funcion declarada al directorio de funciones
            param func_name: nombre de la función
            param t: tipo de retorno de la función(incluido void)
        """
        self.functions_directory[func_name] = FunctionDirectoryRecord(
            name = func_name,
            return_type= t,
            address = len(self.quadruples)
        )
        self.current_function = func_name

    def set_parameters(self, parameters):
        """
            Función que agrega los parametros a la funcion actual 
            que se esta procesando en compilación

            param parameters: lista de parametros con estructura (nombre de parametro, tipo de parametro)
        """
        parameters.reverse()
        for (param_name, param_var_type) in parameters:
            address = self.memory.create_local_address(param_var_type)
            self.functions_directory[self.current_function].add_param((param_name, param_var_type, address))
            self.current_var_table[param_name] = VariableTableRecord(
                name = param_name,
                type = param_var_type,
                address = address
                )
            self.add_function_local_var_size(param_var_type, 1)
            

    def set_variable(self, var_name, var_type, rows=1, columns=1):
        """
            Función que agrega una variable declarada a la
            tabla de variables. Se calcula el tamaño de la variable
            multiplicando rows y columns(que por default es 1)

            param var_name: nombre de la variable
            para var_type: tipo de la variable
            param rows: usado si es un arreglo o matriz
            param columns: usado si es una matriz
        """
        address = self.memory.create_local_address(var_type, size=(rows * columns))
        self.current_var_table[var_name] = VariableTableRecord(
            name = var_name,
            type = var_type,
            address = address,
            dimensions = (rows, columns)
            )
        self.add_function_local_var_size(var_type, rows * columns)
        self.create_constant(rows, VarType.INT)
        self.create_constant(columns, VarType.INT)

    def create_constant(self, value, type):
        """
            Función que crea una constante en caso de no encontrarse en
            la tabla de variables constantes. Si ya esta declarada en la tabla
            de variables constantes, regresa su direccion de memoria

            param value: valor de la constante
            param type: tipo de la constante
        """
        constant_address = self.constants_table.get(value)
        if not constant_address:
            constant_address = self.memory.create_constant_address(type)
            self.constants_table[value] = constant_address
    
    def get_constant(self, value):
        """
            Función que regresa la dirección de una variable 
            constante de la tabla de variables constantes

            param value: valor de la constante
        """
        constant_address = self.constants_table.get(value)
        if constant_address != None:
            return constant_address
        else:
            raise Exception("Compilation eror: Constant variable, which value is:", value, " is not registered yet.")

    def consume_operator(self, operator):
        """
            Función que agrega un operador a la pila de operadores

            param operator: el operador que se requiere agregar, de tipo Operator
        """
        self.stack.push_operator(operator)

    def consume_operand(self, operand, var_type=None, is_constant=False):
        """
            Función que agrega un operando a la pila de operandos
            tomando en cuenta si dicha variable es constante o no

            param operand: el nombre del operando o el valor(en caso de que sea constante)
            param is_constant: indica si el operando es constante
        """
        if is_constant:
            self.consume_constant_operand(operand, var_type)
        else:
            self.consume_var_operand(operand)

    def consume_constant_operand(self, constant, c_type):
        """
            Función que agrega un operando constante a la pila de 
            operandos

            param constant: valor del constante
            param c_type: tipo de constante
        """
        constant_address = self.constants_table.get(constant)
        if not constant_address:
            constant_address = self.memory.create_constant_address(c_type)
            self.constants_table[constant] = constant_address
        self.stack.push_operand(constant_address, c_type)

    def consume_var_operand(self, operand):
        """
            Función que agrega una variable a la pila de operandos

            param operand: nombre de la variable (el operando)
        """
        try:
            var = self.var_lookup(operand)
            if var.address:
                self.stack.push_operand(var.address, var.type)
            else:
                self.stack.push_operand(var.name, var.type)
        except Exception:
            raise Exception("Compilation error: Variable: ", operand, "does not exist.")

    def consume_array_usage(self, array_name, index_operand):
        """
            Función que se encarga de agregar el valor de un indice de un arreglo
            a una variable.

            param array_name: nombre del arreglo
            para index_operand: tupla con informácion del índice que se pide del arreglo
                con forma (dirección de memoria del índice, tipo de variable del índice)         
        """
        # Se verifica que el arreglo exista ya declarado
        var = self.var_lookup(array_name)
        if var is None:
            raise Exception("Compilation error: Array: ",array_name ," does not exist. Can not be assign to a variable.")
        base_address = var.address
        index_address = index_operand[0]
        index_type = index_operand[1]

        # Se verifica que el índice del arreglo sea de tipo entero
        if index_type != VarType.INT:
            raise Exception('Compilation Error: array index is not of type int!')
        
        # Agregar operador VERIFY para verificar que el indice este en rango
        rows_address = self.constants_table.get(var.dimensions[0])
        verify_quadruple = Quadruple(Operator.VERIFY, index_address, None, rows_address)
        self.quadruples.append(verify_quadruple)

        # Se hace la suma de la direccion base
        constant_address = self.get_constant(base_address)
        pointer_to_temp_address = self.memory.create_pointer_address(var.type)
        add_array_base_quadruple = Quadruple(Operator.SUM, index_address, constant_address, pointer_to_temp_address)
        self.quadruples.append(add_array_base_quadruple)

        # Push pointer de arreglo a stack de operandos
        self.stack.push_operand(pointer_to_temp_address, var.type)

    def consume_matrix_usage(self, matrix_name, index_operand):
        """
            Función que se encarga de agregar el valor de una casilla de una matriz
            a una variable.

            param matrix_name: nombre de la matriz
            param index_operando: tupla conteniendo el operando del índice de
                la fila y la columna de la matriz.  
        """
        # Se verifica que la matriz exista
        var = self.var_lookup(matrix_name)
        if var is None:
            raise Exception("Compilation error: Matrix: ",matrix_name, " does not exist. Can not be assign to a variable")
       
        matrix_base_address = var.address
        matrix_first_index = index_operand[0]
        matrix_second_index = index_operand[1]

        # Se obtiene la dirección de ambos índices de la matriz
        matrix_first_index_address = matrix_first_index[0]
        matrix_second_index_address = matrix_second_index[0]

        # Se obtiene el tipo de variable de ambos índices de la matriz
        matrix_first_index_type = matrix_first_index[1]
        matrix_second_index_type = matrix_second_index[1]

        # Se verifica que los índices sean de tipo entero
        if matrix_first_index_type != VarType.INT:
            raise Exception("Compilation error: Matrix ",matrix_name, " first index is not an int")
        if matrix_second_index_type != VarType.INT:
            raise Exception("Compilation error: Matrix ",matrix_name, " second index is not an int")

        matrix_type = var.type

        # Agregando VERIFY de la primera dimension para 
        # verificar que el índice este en el rango
        matrix_row_address = self.constants_table.get(var.dimensions[0])
        verify_quadruple = Quadruple(Operator.VERIFY, matrix_first_index_address, None, matrix_row_address)
        self.quadruples.append(verify_quadruple)

        # Generando el valor M1 y creando un valor constante de ello
        matrix_m_one = int(((var.dimensions[0]) * (var.dimensions[1])) / (var.dimensions[0]))
        matrix_m_one_constant_address = self.get_constant(matrix_m_one)
        
        # Generando el cuádruplo MULTIPLY de s1 * m1
        matrix_temp_multiply = self.create_temp_var(VarType.INT)
        self.increment_current_function_temp_size(VarType.INT)
        matrix_temp_multiply_address = self.current_var_table[matrix_temp_multiply].address
        multiply_m_one_quadruple = Quadruple(Operator.MULTIPLY, matrix_first_index_address, matrix_m_one_constant_address, matrix_temp_multiply_address)
        self.quadruples.append(multiply_m_one_quadruple)
        
        # Agregando Verify de la segunda dimension s2
        matrix_columns_address = self.constants_table.get(var.dimensions[1])
        verify_quadruple = Quadruple(Operator.VERIFY, matrix_second_index_address, None, matrix_columns_address)
        self.quadruples.append(verify_quadruple)

        # Sumando s1*m1 + s2
        temp_sum = self.create_temp_var(VarType.INT)
        self.increment_current_function_temp_size(VarType.INT)
        temp_sum_address = self.current_var_table[temp_sum].address
        sum_quadruple = Quadruple(Operator.SUM, matrix_temp_multiply_address, matrix_second_index_address, temp_sum_address)
        self.quadruples.append(sum_quadruple)

        # Haciendo suma de direccion base s1*m1 + s2 + dirBase
        matrix_constant_address = self.get_constant(matrix_base_address)
        pointer_to_temp_address = self.memory.create_pointer_address(matrix_type)
        add_matrix_base_quadruple = Quadruple(Operator.SUM, temp_sum_address, matrix_constant_address, pointer_to_temp_address)
        self.quadruples.append(add_matrix_base_quadruple)

        #Push pointer a stack de operandos
        self.stack.push_operand(pointer_to_temp_address, matrix_type)

    # Buscar variable en tabla de variables locales y globales
    def var_lookup(self, var_name):
        """
            Función que se encarga de buscar si una variable esta 
            declarada, ya sea en la tabla de variables globales o 
            en la tabla de variables locales   

            param var_name: nombre de la variable   
        """
        var = self.current_var_table.get(var_name)
        if var:
            return var
        var = self.global_var_table[var_name]
        return var

    def handle_read(self, id):
        """
            Función que agrega el cuadruplo con el operador READ a la 
            lista de cuadruplos

            param id: nombre de la variable
        """
        var = self.var_lookup(id)
        quadruple = Quadruple(Operator.READ, None, None, var.address)
        self.quadruples.append(quadruple)

    def handle_print(self):
        """
            Función que agrega el cuadruplo el operador PRINT a la 
            lista de cuadruplos
        """
        if self.stack.operands:
            var_name = self.stack.operands.pop()
            quadruple = Quadruple(Operator.PRINT, None, None, var_name)
            self.quadruples.append(quadruple)

    def create_temp_var(self, t_type):
        """
            Función que crea una variable temporal y la agrega
            a la tabla de variables locales 
            
            param t_type: tipo de variable temporal
        """
        name = "temp_" + str(self.temp_index)
        address = self.memory.create_temporal_address(t_type)
        self.current_var_table[name] = VariableTableRecord(
            name = name,
            type = t_type,
            address = address
        )
        self.temp_index = self.temp_index + 1
        return name

    def set_quadruple(self):
        """
            Función que crea una cuadruplo y lo añade a la 
            lista de cuadruplos
        """
        if len(self.stack.operands) >= 2 and len(self.stack.operators) >= 1:
            right_operand = self.stack.operands.pop()
            left_operand = self.stack.operands.pop()
            operator = Operator(self.stack.operators.pop())
            right_operand_type = self.stack.types.pop()
            left_operand_type = self.stack.types.pop()
            cube_result = self.cube[right_operand_type][left_operand_type][operator]

            # Si el resultado del cubo semantico no es error, crea el cuadruplo
            if cube_result != "err":
                temp = self.create_temp_var(cube_result)
                temp_address = self.current_var_table[temp].address
                temp_type = self.current_var_table[temp].type

                # Actualiza el count de temporales dependiendo el tipo
                self.increment_current_function_temp_size(temp_type)
                
                quadruple = Quadruple(Operator(operator), left_operand, right_operand, temp_address)
                self.quadruples.append(quadruple)
                self.consume_operand(temp, cube_result)
            else:
                raise Exception("Compilation error: Setting quadruple: type mismatch between operand", left_operand, "and", right_operand)
        else:
            raise Exception("Compilation error: Not enough operands and operators to create quadruples.")

    def get_variable(self, var_name):
        var = self.current_var_table[var_name]
        if var is None:
            raise Exception("Compialtion error: The variable is not declared.")
        return var


    def add_var_operand(self, var_name):
        """
            Función que asigna un valor a una variable

            param var_name: nombre de la variable
        """
        var = self.current_var_table[var_name]
        if var is None:
            raise Exception("Compilation error: The variable is not declared. Can not assign a value to this variable.")
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
            # Si el resultado del cubo semantico no es error, crea el cuadruplo
            if cube_result != "err":
                quadruple = Quadruple(Operator(operator), right_operand, None, left_operand)
                self.quadruples.append(quadruple)
            else:
                raise Exception("Compilation error: Setting variable a value: type mismatch between operand ", left_operand, " type ", left_operand_type,  " and operand ", right_operand, " type ", right_operand_type)

    def handle_array_assign(self, var_name):
        """
            Función que asigna un valor a un índice de un arreglo

            param var_name: nombre del arreglo
        """
        var = self.current_var_table[var_name]
        if var is None:
            raise Exception("Compilation error: The array named: " ,var_name, " is not declared. Can not assign a variable this array.")
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
                    raise Exception("Compilation error: Can not assign variable to array because of type mismatch between operand ", array_base_address, " type " ,array_type,  "and operand ", right_operand, " type " ,right_operand_type)
            else:
                raise Exception("Compilation error: The array index type must be an integer. Can not assign a variable to this array.")

    def handle_matrix_assign(self, var_name):
        """
            Función que asigna un valor a una casilla de una matriz

            param var_name: nombre de la matriz
        """
        var = self.current_var_table[var_name]
        if var is None:
            raise Exception("Compilation error: The matrix named: " ,var_name, " is not declared. Can not assign a variable this matrix.")
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
                    m_one = int(((var.dimensions[0]) * (var.dimensions[1])) / (var.dimensions[0]))
                    m_one_constant = self.create_constant(m_one, VarType.INT)
                    m_one_constant_address = self.get_constant(m_one)
                    temp_multiply = self.create_temp_var(VarType.INT)
                    self.increment_current_function_temp_size(VarType.INT)
                    temp_multiply_address = self.current_var_table[temp_multiply].address
                    multiply_m_one_quadruple = Quadruple(Operator.MULTIPLY, matrix_first_index_operand, m_one_constant_address, temp_multiply_address)
                    self.quadruples.append(multiply_m_one_quadruple)

                    # Agregando Verify de la segunda dimension s2
                    columns_address = self.constants_table.get(var.dimensions[1])
                    verify_quadruple = Quadruple(Operator.VERIFY, matrix_second_index_operand, None, columns_address)
                    self.quadruples.append(verify_quadruple)
                    
                    # Sumando s1*m1 + s2
                    temp_sum = self.create_temp_var(VarType.INT)
                    self.increment_current_function_temp_size(VarType.INT)
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
                    raise Exception("Compilation error: Can not assign variable to matrix because of type mismatch between operand ", matrix_base_address, " type " ,matrix_type,  "and operand ", right_operand, " type " ,right_operand_type)
            else:
                raise Exception("Compilation error: Both matrix indexes types must be integers. Can not assign a variable to this matrix.")

    def set_initial_while(self):
        """
            Función que maneja las acciones semánticas al inicio de un estatuto while.
            Agrega a la pila de saltos la ubicación del while y
            luego hace acciones para establecer un bloque condicional.
        """
        # Jump index para regresar a evaluar la condicion del while (al cuádruplo de la condición)
        jump_index = len(self.quadruples) - 1
        self.jumps_stack.append(jump_index)
        self.set_conditional_block()

    def set_conditional_block(self):
        """
            Función que hace acciones semánticas para 
            empezar un bloque condicional (if, while).

            Checa de la pila de operandos si el último
            es de tipo booleano, si lo es, agrega un cuádruplo con
            operador GOTOF y agrega a la pila de saltos su ubicación.
        """
        if self.stack.operands:
            result = self.stack.operands.pop()
            if self.stack.types.pop() == VarType.BOOL:
                quadruple = Quadruple(Operator.GOTOF, result, None, None)
                self.quadruples.append(quadruple)
                jump_index = len(self.quadruples) - 1
                self.jumps_stack.append(jump_index)
            else:
                raise TypeError("Compilation error: The result of the conditional operation must be of type bool.")
        else:
            raise Exception("Compilation error: Not enough operands to resolve the conditional operation.")

    def set_end_of_if(self):
        """
            Función ejecutada al terminar el bloque del
            estatuto IF.

            Saca la ubicación del GOTOF del IF de la pila de saltos.
        """
        if self.jumps_stack:
            quadruple_index_to_set = self.jumps_stack.pop()
            final_jump_index = len(self.quadruples)
            self.set_final_jump(quadruple_index_to_set, final_jump_index)
        else:
            raise Exception("Compilation error: Jump stack is empty. Can not set the end of IF.")

    def set_else(self):
        """
            Función ejecutada al inicio de un bloque ELSE.
            Se agrega un cuádruplo con operador GOTO
            y se asigna la ubicación actual
            al GOTOF de la condición del IF.
        """
        quadruple = Quadruple(Operator.GOTO, None, None, None)
        self.quadruples.append(quadruple)

        if self.jumps_stack:
            quadruple_index_to_set = self.jumps_stack.pop()
            self.jumps_stack.append(len(self.quadruples) - 1)
            self.set_final_jump(quadruple_index_to_set, len(self.quadruples))
        else:
            raise Exception("Compilation error: Jump stack is empty. Can not set the end of ELSE.")

    def set_end_of_while(self):
        """
            Función ejecutada al final del bloque del WHILE.
            Se obtiene la ubicación de cuádruplos en donde
            se evalua la expresión booleana y en donde
            esta el GOTOF.

            Se agrega un operador GOTO para regresar a evaluar la condición.
        """
        end_jump_index = self.jumps_stack.pop()
        condition_jump_index = self.jumps_stack.pop()
        quadruple = Quadruple(Operator.GOTO, None, None, condition_jump_index)
        self.quadruples.append(quadruple)        
        self.set_final_jump(end_jump_index, len(self.quadruples))

    def set_final_jump(self, quadruple_index_to_set, final_jump_index):
        """
            Función que establece el resultado de un
            cuádruplo con operador de salto, es decir,
            a donde va a saltar.

            param quadruple_index_to_set: cuádruplo que se modifica
            param final_jump_index: destino de salto
        """
        self.quadruples[quadruple_index_to_set].temp_result = final_jump_index

    def set_function_call(self, func_name, arguments):
        """
            Función ejecutada cada vez que se llama una función en PPC.

            param func_name: nombre de la función para ser buscada en el directorio.
            param arguments: lista de argumentos, siendo cada uno una tupla (direcciónDeArgumento, tipoDeArgumento)
        """
        function = self.functions_directory[func_name]
        function_params_types = []
        arguments_types = []

        #Revisar funcion en el directorio de funciones
        if function is None:
            raise Exception("Compilation error: The function ", func_name ," is not declared. Can not use it.")
        else:
            #Revisar numero de parametros
            if len(arguments) != len(function.params):
                raise Exception("Compilation error: The number of parameters the function ", function.name, " requires is incorrect.")
            else:
                #Revisar el tipo de parametros
                for param in (function.params):
                    function_params_types.append(param[1])

                for argument in arguments:
                    arguments_types.append(argument[1])

                #TODO revisar más casos que no cause problemas por este reverse
                arguments_types.reverse()

                if function_params_types != arguments_types:
                    raise Exception("Compilation error: The type of parameters the function ", function.name ," requires is incorrect.")
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
        """
            Función ejecutada cuando se encuentra con un estatuto RETURN.
            Valida primero que el tipo de función en donde
            se encuentra espera un RETURN.

            Si es asi, guarda su resultado en la variable global de la función.
        """
        function = self.functions_directory[self.current_function]
        operand = self.stack.operands.pop()
        operand_type = self.stack.types.pop()

        if function.return_type.name == operand_type.name:
            function_global_address = self.global_var_table[function.name].address
            quad = Quadruple(Operator.RETURN, operand, None, function_global_address)
            self.quadruples.append(quad)
        else:
            raise Exception("Compilation error: The return type the function requires is incorrect. Can not return this type of value.")

    def add_function_local_var_size(self, var_type, size, func_name=None):
        """
            Función que incrementa el número de variables locales
            que requiere la función actual (o la función que se especifíca).

            param var_type: tipo de variable local que se quiere incrementar
            param size: cantidad que se quiere inncrementar.
            param func_name: nombre de la función que se quiere modificar, si se omite, se usa 
                la función actual en el proceso de compilación.
        """
        function_name = func_name if func_name != None else self.current_function
        function = self.functions_directory[function_name]
        if var_type == VarType.INT:
            function.local_var_int_size += size
        elif var_type == VarType.FLOAT:
            function.local_var_float_size += size
        elif var_type == VarType.CHAR:
            function.local_var_char_size += size
        elif var_type == VarType.BOOL:
            function.local_var_bool_size += size

    def increment_current_function_temp_size(self, temp_type):
        """
            Similar a la función add_function_local_var_size,
            sin embargo, esta solo incrementa por uno
            el número de variables temporales que requiere
            la función actual.

            param temp_type: tipo de variable temporal que necesita la función
        """
        function = self.functions_directory[self.current_function]
        if temp_type == VarType.INT:
            function.temp_var_int_size += 1
        elif temp_type == VarType.FLOAT:
            function.temp_var_float_size += 1
        elif temp_type == VarType.CHAR:
            function.temp_var_char_size += 1
        elif temp_type == VarType.BOOL:
            function.temp_var_bool_size += 1

    def end_func(self):
        """
            Función que se ejecuta al terminar el bloque de una función.
            Se agrega un cuádruplo con operador ENDFUNC y
            se resetea la memoria local y temporal (empezarlas de 0)
        """
        function = self.functions_directory[self.current_function]
        if function is None:
            print("The function is not declared. Have reached the end of the function and can not continue compiling.")
        quadruple = Quadruple(Operator.ENDFUNC, None, None, None)
        self.quadruples.append(quadruple)
        self.memory.reset_local_and_temp_memory()
        self.current_var_table = dict()

    def get_number_of_pointers_used(self):
        """
            Función utilizada al hacer el archivo de compilación
            que obtiene el número de apuntadores usados a lo largo
            de todo el archivo PPC
        """
        return self.memory.get_pointers_block_size()

    """
        Los siguientes métodos son usados para
        imprimir de forma legible los cuádruplos,
        la tabla de constantes, y la tabla de globales.

        Utilizado para debugging.
    """
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