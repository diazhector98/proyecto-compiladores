from enum import Enum

"""
    Clase Enum que contien los tipos de variables que se manejan en la máquina virtual
"""
class VarType(Enum):
    INT = 'int'
    FLOAT = 'float'
    CHAR = 'char'
    BOOL = 'bool'