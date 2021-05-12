
class Quadruple:
    operator: str
    left_operand: str
    right_operand: str
    temp_result: str

    def __init__(self, output_line):
        elements = output_line.split(' ')
        elements = [e for e in elements if e != '']
        print(elements)