from dataclasses import dataclass

"""
Clase del objeto de un cuádruplo para crear la lista de cuádruplos
operator: operador a utilizar
left_operand: operando izquierdo
right_operand: operando derecho
temp_result: resultado del operando izquierdo con el derecho tomando
en cuenta el 'operator'
"""
@dataclass
class Quadruple:
    operator: str
    left_operand: str
    right_operand: str
    temp_result: str

    def __str__(self) -> str:
        left_operand = self.left_operand if self.left_operand != None else -1
        right_operand = self.right_operand if self.right_operand != None else -1
        result = self.temp_result if self.temp_result != None else -1
        return "{:<12} {:<10} {:<10} {:<10}".format(self.operator.name, str(left_operand), str(right_operand), str(result))
