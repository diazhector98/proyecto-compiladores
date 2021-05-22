from virtual_machine.file_reader import FileReader
from virtual_machine.memory.virtual_machine_memory import VirtualMachineMemory
from virtual_machine.common.operator import Operator
from virtual_machine.operators_handlers import handle_arithmetic_operator, handle_boolean_operator
class VirtualMachine:
    
    """
    quad_index = Contabiliza el cuadruplo en el que se encuentra
    go_to_f_index_to_go = Index a llegar en caso de que go_to_f_activated sea verdadero 
    go_to_f_activated = Bool para saber si puedo acceder los cuadruplos que vienen despues del GoToFo o no
    can_read_else = Bool para saber si puedo acceder a los cuadruplos de Else
    go_to_index_to_go = Index a llegar en caso de que go_to_activated sea verdadero 
    go_to_activated = Bool para saber si puedo acceder los cuadruplos que vienen despues del GoTo o no

    """
    
    quad_index = 0
    go_to_f_index_to_go = -1
    go_to_f_activated = False
    can_read_else = False
    go_to_index_to_go = -1
    go_to_activated = False

    def __init__(self, filename):
        [functions, constants, quadruples] = FileReader(filename)
        self.functions = functions
        self.constants = constants
        self.quadruples = quadruples
        self.memory = VirtualMachineMemory(constants)
        
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

    def go_to_next_quadruple(self):
        self.quad_index += 1

    def jump_to_quadruple(self, quadruple_index):
        self.quad_index = quadruple_index