from dataclasses import dataclass

@dataclass
class Quadruple:
    operator: str
    left_operand: str
    right_operand: str
    temp_result: str

    def __str__(self) -> str:
        return "{:<12} {:<10} {:<10} {:<10}".format(self.operator.name, str(self.left_operand), str(self.right_operand), str(self.temp_result))
