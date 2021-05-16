
class Quadruple:
    index: int
    operator: str
    left_operand: str
    right_operand: str
    temp_result: str

    def __init__(self, output_line):
        string_elements = output_line.split(' ')
        self.string_elements = [e for e in string_elements if e != '']
        self.process_string_elements()

    def process_string_elements(self):
        [str_operator, str_left_operand, str_right_operand, str_result] = self.string_elements
        self.operator = str_operator
        self.left_operand = int(str_left_operand)
        self.right_operand = int(str_right_operand)
        # TODO: Manejar todos resultados como ints o averiguar como manejar nombres de funciones
        self.result = str_result

    def __str__(self):
        return "{:<12} {:<7} {:<7} {:<7}".format(self.operator, self.left_operand, self.right_operand, self.result)