from enum import Enum

"""
    Clase Enum que contiene los tipos de operadores que manejan los cuádruplos
    del archivo generado en compilación.
"""
class Operator(Enum):
    SUM = "SUM"
    MINUS = "MINUS"
    DIVIDE = "DIVIDE"
    MULTIPLY = "MULTIPLY"
    LT = "LT"
    GT = "GT"
    LTE = "LTE"
    GTE = "GTE"
    EQUAL = "EQUAL"
    NE = "NE"
    READ = "READ"
    PRINT = "PRINT" 
    ASSIGN = "ASSIGN"
    GOTO = 'GOTO'
    GOTOF = 'GOTOF'
    GOSUB = 'GOSUB'
    ERA = 'ERA'
    PARAMETER = 'PARAMETER'
    ENDFUNC = 'ENDFUNC'
    RETURN = 'RETURN'
    VERIFY = 'VERIFY'
