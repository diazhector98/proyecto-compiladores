from enum import Enum

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
    AND = "&&"
    OR = "||"
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
