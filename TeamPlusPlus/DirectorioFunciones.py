from dataclasses import dataclass
from enum import Enum

class VarType(Enum):
    INT = 'int'
    FLOAT = 'float'
    CHAR = 'char'
    BOOL = 'bool'

class FuncReturnType(Enum):
    INT = 'int'
    FLOAT = 'float'
    CHAR = 'char'
    VOID = 'void'
    BOOL = 'bool'

"""
Clase para guardar datos de una funcion.
Objetos de esta clase se guardan en el directorio de funciones.
name: Nombre de la función
return_type: Tipo de retorno (void, int, char, etc...)
param_types: Lista de los tipos de parametros esperados
"""
@dataclass
class FunctionDirectoryRecord:
    name: str
    return_type: FuncReturnType
    param_types: [str] = None

"""
Clase para guardar datos de una registro de variable.
Objetos de esta clase se guardan en la tabla de variables
name: nombre de la variable
type: tipo de la variable
"""
@dataclass
class VariableTableRecord:
    name: str
    type: VarType