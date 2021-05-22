from enum import Enum

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
    AND = "AND"
    OR = "OR"
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
