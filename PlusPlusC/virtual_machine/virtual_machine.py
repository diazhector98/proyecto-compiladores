from virtual_machine.file_reader import FileReader
from virtual_machine.memory.virtual_machine_memory import VirtualMachineMemory
from virtual_machine.common.operator import Operator
class VirtualMachine:
    def __init__(self, filename):
        [functions, constants, quadruples] = FileReader(filename)
        self.functions = functions
        self.constants = constants
        self.quadruples = quadruples
        self.memory = VirtualMachineMemory(constants)

    def run(self):
        for quadruple in self.quadruples:
            operator = quadruple.operator
            left_operand = quadruple.left_operand
            right_operand = quadruple.right_operand
            result = quadruple.result

            if self.is_arithmetic_operator(operator):
                self.handle_arithmetic_operator(quadruple)

            if self.is_boolean_operator(operator):
                self.handle_boolean_operator(quadruple)

            if operator == Operator.ASSIGN:
                value = self.memory.read(left_operand)
                self.memory.write(result, value)
            if operator == Operator.PRINT:
                value = self.memory.read(result)
                print(value)
            if operator == Operator.READ:
                capture = input("Waiting input: ")
                self.memory.write(result, capture)

    def is_arithmetic_operator(self, operator):
        return operator in [Operator.SUM, Operator.MULTIPLY, Operator.MINUS, Operator.DIVIDE]

    def handle_arithmetic_operator(self, quadruple):
        operator = quadruple.operator
        left_operand = quadruple.left_operand
        right_operand = quadruple.right_operand
        result = quadruple.result

        left_operand_value = self.memory.read(left_operand)
        right_operand_value = self.memory.read(right_operand)

        if operator == Operator.SUM:
            operation_outcome = left_operand_value + right_operand_value
            self.memory.write(result, operation_outcome)
        if operator == Operator.MULTIPLY:
            operation_outcome = left_operand_value * right_operand_value
            self.memory.write(result, operation_outcome)
        if operator == Operator.MINUS:
            operation_outcome = left_operand_value - right_operand_value
            self.memory.write(result, operation_outcome)
        if operator == Operator.DIVIDE:
            operation_outcome = left_operand_value / right_operand_value
            self.memory.write(result, operation_outcome)

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

    def handle_boolean_operator(self, quadruple):
        operator = quadruple.operator
        left_operand = quadruple.left_operand
        right_operand = quadruple.right_operand
        result = quadruple.result

        left_operand_value = self.memory.read(left_operand)
        right_operand_value = self.memory.read(right_operand)

        if operator == Operator.GT:
            operation_outcome = left_operand_value > right_operand_value
        
        self.memory.write(result, operation_outcome)

            
