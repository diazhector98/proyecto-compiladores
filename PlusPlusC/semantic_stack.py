
"""
Clase para manejar las pilas de la semántica. Se utiliza para generar los cuadruplos


"""

class SemanticStack:
    operators = []
    operands = []
    types = []

    def push_operand(self, operand, type):
        self.operands.append(operand)
        self.types.append(type)
    
    def push_operator(self, operator):
        self.operators.append(operator)