from dataclasses import dataclass

@dataclass
class Quadruple:
    operator: str
    left_operand: str
    right_operand: str
    temp_result: str