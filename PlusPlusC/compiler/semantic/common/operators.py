from enum import Enum

"""
Clase para declarar los operadores que se utilizarán en el proceso
de compilación para crear los cuadruplos
"""
class Operator(Enum):
    SUM = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULTIPLY = "*"
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    EQUAL = "=="
    NE = "!="
    READ = "read"
    PRINT = "print" 
    ASSIGN = "="
    GOTO = 'goto'
    GOTOF = 'gotof'
    GOSUB = 'gosub'
    ERA = 'era'
    PARAMETER = 'parameter'
    ENDFUNC = 'endfunc'
    RETURN = 'return'
    VERIFY = 'verify'
