from virtual_machine.file_reader import FileReader
from virtual_machine.memory.virtual_machine_memory import VirtualMachineMemory
from virtual_machine.common.operator import Operator
from virtual_machine.operators_handlers import handle_arithmetic_operator, handle_boolean_operator
from virtual_machine.activation_record import ActivationRecord


class VirtualMachine:

    def __init__(self, input, read_file=True, terminal=True):
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
        while self.get_quad_index() < len(self.quadruples):
            quad_index = self.get_quad_index()
            quadruple = self.quadruples[quad_index]
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

            elif operator == Operator.PRINT:
                value = self.memory.read(result)
                self.generate_output(value)
                self.go_to_next_quadruple()
            elif operator == Operator.READ:
                capture = input("Waiting input: ")
                self.memory.write(result, capture)
                self.go_to_next_quadruple()
            elif operator == Operator.VERIFY:
                self.handle_array_matrix_operator(quadruple)
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
            Operator.GOSUB,
            Operator.RETURN
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
        return self.call_stack[-1]

    def get_next_activation_record(self):
        return self.activation_records_waiting[-1]

    def handle_gosub(self):
        # El gosub mueve el activation record que 
        # se estaba preparando al tope del call stack
        activation_record = self.activation_records_waiting.pop()
        self.call_stack.append(activation_record)
        self.memory.activation_record = activation_record

    def handle_array_matrix_operator(self, quadruple):
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
        current_activation_record = self.get_current_activation_record()
        return current_activation_record.current_quad_index

    def go_to_next_quadruple(self):
        current_activation_record = self.get_current_activation_record()
        current_activation_record.current_quad_index += 1

    def jump_to_quadruple(self, quadruple_index):
        current_activation_record = self.get_current_activation_record()
        current_activation_record.current_quad_index = quadruple_index

    def print_call_stack(self):
        for ar in self.call_stack:
            print(id(ar), ",", end="")
        print("")

    def generate_output(self, value):
        if self.terminal:
            print(value)
            self.global_output_variable += str(value) + "\n"
        else:
            self.output += str(value) + "\n"
            self.global_output_variable += str(value) + "\n"