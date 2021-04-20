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