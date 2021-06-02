from compiler.semantic.common.DirectorioFunciones import VarType
from compiler.semantic.common.operators import Operator

"""
Reglas del cubo semántico para determinar el resultado de la 
operacion entre dos variables
"""

ERROR = "err"

"""
    En cada una de las reglas, dependiendo del tipo de la
    segunda variable (INT, FLOAT, CHAR, BOOL), se toma en
    cuenta ahora el tipo de operador (SUM, MINUS, MULTIPLY...),
    dependiendo de éste tipo, se determina el resultado del
    cubo semántico. 
"""
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
        Operator.NE: VarType.BOOL,
        Operator.ASSIGN: VarType.INT
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
        Operator.NE: VarType.BOOL,
        Operator.ASSIGN: VarType.INT
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: VarType.BOOL,
        Operator.ASSIGN: VarType.FLOAT
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
        Operator.NE: VarType.BOOL,
        Operator.ASSIGN: VarType.FLOAT
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: VarType.BOOL,
        Operator.ASSIGN: VarType.CHAR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: ERROR,
        Operator.ASSIGN: ERROR
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
        Operator.NE: VarType.BOOL,
        Operator.ASSIGN: VarType.BOOL
    },
}