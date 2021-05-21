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

            if operator == Operator.ASSIGN:
                value = self.memory.read(left_operand)
                self.memory.write(result, value)
            if operator == Operator.PRINT:
                value = self.memory.read(result)
                print(value)
            if operator == Operator.READ:
                capture = input("Waiting input: ")
            
