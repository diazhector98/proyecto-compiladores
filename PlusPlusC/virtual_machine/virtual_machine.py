from virtual_machine.file_reader import FileReader
from virtual_machine.memory.virtual_machine_memory import VirtualMachineMemory
from virtual_machine.common.operator import Operator
from virtual_machine.operators_handlers import handle_arithmetic_operator, handle_boolean_operator
from virtual_machine.activation_record import ActivationRecord
class VirtualMachine:
    """
    quad_index = Contabiliza el cuadruplo en el que se encuentra
    """
    quad_index = 0

    def __init__(self, filename):
        [functions, constants, quadruples] = FileReader(filename)
        self.functions = functions
        self.constants = constants
        self.quadruples = quadruples
        self.call_stack = [ActivationRecord()]
        self.activation_records_waiting = []
        self.memory = VirtualMachineMemory(constants, self.get_current_activation_record())
        
    def run(self):
        while self.quad_index < len(self.quadruples):
            quadruple = self.quadruples[self.quad_index]
            operator = quadruple.operator
            left_operand = quadruple.left_operand
            result = quadruple.result

            if self.is_arithmetic_operator(operator):
                handle_arithmetic_operator(quadruple, self.memory)
                self.go_to_next_quadruple()

            elif self.is_boolean_operator(operator):
                handle_boolean_operator(quadruple, self.memory)
                self.go_to_next_quadruple()

            elif self.is_jump_operator(operator):
                self.handle_jump_operator(quadruple)

            elif self.is_function_operator(operator):
                self.handle_function_operator(quadruple)
                self.go_to_next_quadruple()

            elif operator == Operator.PRINT:
                value = self.memory.read(result)
                print(value)
                self.go_to_next_quadruple()
            elif operator == Operator.READ:
                capture = input("Waiting input: ")
                self.memory.write(result, capture)
                self.go_to_next_quadruple()
            else:
                self.go_to_next_quadruple()

    def is_arithmetic_operator(self, operator):
        return operator in [
            Operator.ASSIGN, 
            Operator.SUM, 
            Operator.MULTIPLY, 
            Operator.MINUS, 
            Operator.DIVIDE
        ]

    def is_boolean_operator(self, operator):
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
        return operator in [
            Operator.ERA,
            Operator.PARAMETER,
            Operator.ENDFUNC,
            Operator.GOSUB
        ]

    def is_jump_operator(self, operator):
        return operator in [
            Operator.GOTO,
            Operator.GOTOF
        ]
            
    def handle_jump_operator(self, quadruple):
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
        operator = quadruple.operator
        left_operand = quadruple.left_operand
        result = quadruple.result

        if operator == Operator.ERA:
            print("Hacer espacio de memoria para la funcion", result)
            activation_record = ActivationRecord(self.functions[result])
            self.activation_records_waiting.append(activation_record)
        elif operator == Operator.PARAMETER:
            next_activation_record = self.get_next_activation_record()
            value = self.memory.read(left_operand)
            next_activation_record.write(result, value)
            print("Quardar ", left_operand , "en parametro", result)
        elif operator == Operator.GOSUB:
            print("Cambio de contexto a la funcion")
        elif operator == Operator.ENDFUN:
            print("Eliminar contexto de la funcion")

    def get_current_activation_record(self):
        return self.call_stack[-1]

    def get_next_activation_record(self):
        return self.activation_records_waiting[-1]

    def go_to_next_quadruple(self):
        self.quad_index += 1

    def jump_to_quadruple(self, quadruple_index):
        self.quad_index = quadruple_index