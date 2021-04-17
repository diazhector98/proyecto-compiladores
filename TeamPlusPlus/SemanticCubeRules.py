from enum import Enum
from DirectorioFunciones import VarType

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

ERROR = "err"

INTEGER_RULES = {
    VarType.INT: {
        Operator.SUM: VarType.INT,
        Operator.MINUS: VarType.INT,
        Operator.MULTIPLY: VarType.INT,
        Operator.DIVIDE: VarType.INT,
        Operator.LT: VarType.BOOL,
        Operator.GT: VarType.BOOL,
        Operator.LTE: VarType.BOOL,
        Operator.GTE: VarType.BOOL,
        Operator.EQUAL: VarType.BOOL,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.FLOAT: {
        Operator.SUM: VarType.FLOAT,
        Operator.MINUS: VarType.FLOAT,
        Operator.MULTIPLY: VarType.FLOAT,
        Operator.DIVIDE: VarType.FLOAT,
        Operator.LT: VarType.BOOL,
        Operator.GT: VarType.BOOL,
        Operator.LTE: VarType.BOOL,
        Operator.GTE: VarType.BOOL,
        Operator.EQUAL: VarType.BOOL,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.CHAR: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.BOOL: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
}

FLOAT_RULES = {
    VarType.INT: {
        Operator.SUM: VarType.FLOAT,
        Operator.MINUS: VarType.FLOAT,
        Operator.MULTIPLY: VarType.FLOAT,
        Operator.DIVIDE: VarType.FLOAT,
        Operator.LT: VarType.BOOL,
        Operator.GT: VarType.BOOL,
        Operator.LTE: VarType.BOOL,
        Operator.GTE: VarType.BOOL,
        Operator.EQUAL: VarType.BOOL,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.FLOAT: {
        Operator.SUM: VarType.FLOAT,
        Operator.MINUS: VarType.FLOAT,
        Operator.MULTIPLY: VarType.FLOAT,
        Operator.DIVIDE: VarType.FLOAT,
        Operator.LT: VarType.BOOL,
        Operator.GT: VarType.BOOL,
        Operator.LTE: VarType.BOOL,
        Operator.GTE: VarType.BOOL,
        Operator.EQUAL: VarType.BOOL,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.CHAR: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.BOOL: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
}

CHAR_RULES = {
    VarType.INT: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.FLOAT: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.CHAR: {
        Operator.SUM: VarType.CHAR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: VarType.BOOL,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.BOOL: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
}

BOOL_RULES = {
    VarType.INT: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.FLOAT: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.CHAR: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: ERROR,
        Operator.AND: ERROR,
        Operator.OR: ERROR
    },
    VarType.BOOL: {
        Operator.SUM: ERROR,
        Operator.MINUS: ERROR,
        Operator.MULTIPLY: ERROR,
        Operator.DIVIDE: ERROR,
        Operator.LT: ERROR,
        Operator.GT: ERROR,
        Operator.LTE: ERROR,
        Operator.GTE: ERROR,
        Operator.EQUAL: VarType.BOOL,
        Operator.AND: VarType.BOOL,
        Operator.OR: VarType.BOOL
    },
}