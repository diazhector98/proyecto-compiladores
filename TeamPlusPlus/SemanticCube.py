from DirectorioFunciones import VarType
from SemanticCubeRules import INTEGER_RULES

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
        VarType.INT: INTEGER_RULES
    }
    
    def __init__(self):
        pass

    def __getitem__(self, first_operand):
        return self.cube[first_operand]

    

