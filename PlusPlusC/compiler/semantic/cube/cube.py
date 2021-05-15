from compiler.semantic.common.DirectorioFunciones import VarType
from compiler.semantic.cube.rules import INTEGER_RULES, FLOAT_RULES, CHAR_RULES, BOOL_RULES

"""
Cubo semántico para verificar el uso de operadores y operandos

Uso:

cube[PRIMER_OPERANDO][SEGUNDO_OPERANDO][OPERADOR]

Ejemplo:

cube = SemanticCube()
cube_result = cube[VarType.INT][VarType.FLOAT][Operator.SUM]
print(cube_result) # VarType.FLOAT

"""
class SemanticCube:
    cube = {
        VarType.INT: INTEGER_RULES,
        VarType.FLOAT: FLOAT_RULES,
        VarType.CHAR: CHAR_RULES,
        VarType.BOOL: BOOL_RULES
    }
    
    def __init__(self):
        pass

    def __getitem__(self, first_operand):
        print(first_operand)
        return self.cube[first_operand]

    

