from virtual_machine.file_reader import FileReader
from virtual_machine.memory.virtual_machine_memory import VirtualMachineMemory
from virtual_machine.common.operator import Operator
from virtual_machine.operators_handlers import handle_arithmetic_operator, handle_boolean_operator
from virtual_machine.activation_record import ActivationRecord

"""
Esta clase maneja la ejecución del archivo de compilación. 
Después de ser inicializada con los datos de entrada, 
se pueden ejecutar los cuádruplos mediante el método "run".

Esta clase tiene dos atributos importantes:

1. El "call_stack", que maneja el contexto actual de ejecución
2. La "memory", que maneja la escritura y lectura en la memoria
"""
class VirtualMachine:
    """
        param input: es por default el nombre del archivo de compilación.
        param: read_file se pasa como negativo si se desea pasar una variable string como "input"
        param: terminal se hace falso si se desea que el output de ejecuciónse 
        guarde en una variable de la clase (self.output)
    """
    def __init__(self, input, read_file=True, terminal=True):
        self.output = ''
        self.read_file = read_file
        self.terminal = terminal
        [pointers, functions, constants, constants_sizes, quadruples] = FileReader(input, read_file=read_file)
        self.functions = functions
        self.constants = constants
        self.quadruples = quadruples
        main_function = functions['main']
        self.call_stack = [ActivationRecord(main_function, main_function.start_quadruple_index)]
        self.activation_records_waiting = []
        global_function = functions['global']
        self.memory = VirtualMachineMemory(pointers, global_function, constants, constants_sizes, self.get_current_activation_record())

    global_output_variable = ""

    def run(self):
        """
            Esta función pasa por todos los cuádruplos por medio de un ciclo while y los ejecuta.
            Checa el tipo de operador es y luego los ejecuta apropiadamente.
        """
        while self.get_quad_index() < len(self.quadruples):
            quad_index = self.get_quad_index()
            quadruple = self.quadruples[quad_index]
            operator = quadruple.operator
            left_operand = quadruple.left_operand
            result = quadruple.result

            if self.is_arithmetic_operator(operator):
                handle_arithmetic_operator(quadruple, self.memory)
                self.go_to_next_quadruple()

            elif self.is_conditional_operator(operator):
                handle_boolean_operator(quadruple, self.memory)
                self.go_to_next_quadruple()

            elif self.is_jump_operator(operator):
                self.handle_jump_operator(quadruple)

            elif self.is_function_operator(operator):
                self.handle_function_operator(quadruple)

            elif operator == Operator.PRINT:
                value = self.memory.read(result)
                self.generate_output(value)
                self.go_to_next_quadruple()
            elif operator == Operator.READ:
                capture = input("Waiting input: ")
                self.memory.write(result, capture)
                self.go_to_next_quadruple()
            elif operator == Operator.VERIFY:
                self.handle_verify_operator(quadruple)
            else:
                self.go_to_next_quadruple()

    def is_arithmetic_operator(self, operator):
        """
        param operator: tipo de operador de un cuádruplo 
        return : regresa si el operador hace una operación aritmética
        """
        return operator in [
            Operator.ASSIGN, 
            Operator.SUM, 
            Operator.MULTIPLY, 
            Operator.MINUS, 
            Operator.DIVIDE
        ]

    def is_conditional_operator(self, operator):
        """
        param operator: tipo de operador de un cuádruplo 
        return : regresa si el operador es de tipo condicional y genera un booleano
        """
        return operator in [
            Operator.LT, 
            Operator.GT, 
            Operator.LTE,
            Operator.GTE,
            Operator.EQUAL,
            Operator.NE,
            Operator.AND,
            Operator.OR
        ]

    def is_function_operator(self, operator):
        """
        param operator: tipo de operador de un cuádruplo 
        return : regresa si el operador funciona para el manejo de funciones.
        """
        return operator in [
            Operator.ERA,
            Operator.PARAMETER,
            Operator.ENDFUNC,
            Operator.GOSUB,
            Operator.RETURN
        ]

    def is_jump_operator(self, operator):
        """
        param operator: tipo de operador de un cuádruplo 
        return : regresa si el operador genera un salto
        """
        return operator in [
            Operator.GOTO,
            Operator.GOTOF
        ]
            
    def handle_jump_operator(self, quadruple):
        """
            Función que maneja operadores que generan un salto de cuádruplos.
            Se lee la dirección del operador izquierdo y se salta apropiadamente
            según su valor booleano.
            param operator: cuádruplo con operador GOTOF o GOTO
        """

        operator = quadruple.operator
        left_operand = quadruple.left_operand
        result = quadruple.result
        
        if operator == Operator.GOTOF:
            left_operand_value = self.memory.read(left_operand)
            if left_operand_value == False:
                self.jump_to_quadruple(result)
            else:
                self.go_to_next_quadruple()
        elif operator == Operator.GOTO:
            self.jump_to_quadruple(result)
        else:
            self.go_to_next_quadruple()

    def handle_function_operator(self, quadruple):
        """
            Función que maneja operadores relacionados a funciones.
            Aquí se genera un nuevo ActivationRecord al procesar el operador ERA.
            param operator: cuádruplo con operador relacionado al manejo de funciones
        """
        operator = quadruple.operator
        left_operand = quadruple.left_operand
        result = quadruple.result
        if operator == Operator.ERA:
            function = self.functions[result]
            activation_record = ActivationRecord(function, function.start_quadruple_index)
            self.activation_records_waiting.append(activation_record)
            self.go_to_next_quadruple()
        elif operator == Operator.PARAMETER:
            next_activation_record = self.get_next_activation_record()
            value = self.memory.read(left_operand)
            next_activation_record.write(result, value)
            self.go_to_next_quadruple()
        elif operator == Operator.GOSUB:
            self.go_to_next_quadruple()
            self.handle_gosub()
        elif operator == Operator.ENDFUNC:
            s = self.call_stack.pop()
            self.memory.activation_record = self.get_current_activation_record()
        elif operator == Operator.RETURN:
            value = self.memory.read(left_operand)
            self.memory.write(result, value)
            f = self.call_stack.pop()
            self.memory.activation_record = self.get_current_activation_record()

    def get_current_activation_record(self):
        """
            return: Se regresa el ActivationRecord arriba de la pila de ejecución.
        """
        return self.call_stack[-1]

    def get_next_activation_record(self):
        """
            return: Se regresa el ActivationRecord que se esta preparando 
            para pasar a la pila de ejecución. Esta función se usa para procesar 
            el operador de PARAMETER y saber en que memoria local/temporal escribir
            el valor de los parámetros.
        """
        return self.activation_records_waiting[-1]

    def handle_gosub(self):
        """
            Funcion que hace lo necesario para procesar el operador GOSUB.
            1. Obtiene el último ActivationRecord del que se llamo el operador ERA
            2. Se agrega a la pila de ejecución.
            3. Se establece que la memoria local/temporal es ahora de ese ActivationRecord
        """
        activation_record = self.activation_records_waiting.pop()
        self.call_stack.append(activation_record)
        self.memory.activation_record = activation_record

    def handle_verify_operator(self, quadruple):
        """
            Función que maneja el operador VERIFY, que verifica que la posición
            del arreglo esta dentro de sus rangos.

            param quadruple: cuádruplo con operador VERIFY
        """
        operator = quadruple.operator
        left_operand = quadruple.left_operand
        result = quadruple.result

        if operator == Operator.VERIFY:
            left_operand_value = self.memory.read(left_operand)
            result_value = self.memory.read(result)
            if not 0 <= left_operand_value <= result_value:
                raise Exception("Execution error: Index out of bounds")
            self.go_to_next_quadruple()


    def get_quad_index(self):
        """
            Función que obtiene el índice actual de los cuádruplos en la ejecución.
            Se obtiene del ActivationRecord de la pila de ejecución.

            return: índice de ejecución actual de los cuádruplos
        """
        current_activation_record = self.get_current_activation_record()
        return current_activation_record.current_quad_index

    def go_to_next_quadruple(self):
        """
            Función que avanza el índice de ejecución actual de los cuádruplos.
            Obtiene el ActivtionRecord de la pila de ejecución y se incrementa
            su atributo de current_quad_index
        """
        current_activation_record = self.get_current_activation_record()
        current_activation_record.current_quad_index += 1

    def jump_to_quadruple(self, quadruple_index):
        """
            Función que cambia el índice de ejecución de los cuádruplos.
            param quadruple_index : indíce de cuádruplos a donde se quiere cambiar el flujo actual de ejecución
        """
        current_activation_record = self.get_current_activation_record()
        current_activation_record.current_quad_index = quadruple_index

    def generate_output(self, value):
        """
            Función que maneja la salida de algún valor en ejecución.
            Dependiendo de cómo se específico en la inicialización de la clase,
            se imprime en consola o solo se agrega a la variable de la clase
            donde se almacena todo el output de ejecución.
        """
        if self.terminal:
            print(value)
            self.global_output_variable += str(value) + "\n"
        else:
            self.output += str(value) + "\n"
            self.global_output_variable += str(value) + "\n"