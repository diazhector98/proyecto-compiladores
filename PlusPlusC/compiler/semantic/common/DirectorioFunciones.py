from dataclasses import dataclass, field
from enum import Enum

"""
Estos Enums se utilizan para crear los objetos de las variables y funciones
Dichos objetos se utilzan para hacer posible las tablas de variables y el
directorio de funciones
"""
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
return_type: tipo de retorno (void, int, char, etc...)
param_types: lista de los tipos de parametros esperados
address: direccion de memoria asignada a la funcion
"""
@dataclass
class FunctionDirectoryRecord:
    name: str
    return_type: FuncReturnType
    params: [VarType] = field(default_factory=list)
    def add_param(self, param):
        self.params.append(param)
    address: int = None
    temp_var_int_size: int = 0
    temp_var_float_size: int = 0
    temp_var_char_size: int = 0
    temp_var_bool_size: int = 0
    local_var_int_size: int = 0
    local_var_float_size: int = 0
    local_var_char_size: int = 0
    local_var_bool_size: int = 0

    def __str__(self):
        temp_vars_string = "[{},{},{},{}]".format(self.temp_var_int_size, self.temp_var_float_size, self.temp_var_char_size, self.temp_var_bool_size)
        local_vars_string = "[{},{},{},{}]".format(self.local_var_int_size, self.local_var_float_size, self.local_var_char_size, self.local_var_bool_size)
        return "{} {} {} {}".format(self.name, str(self.address), temp_vars_string, local_vars_string)

"""
Clase para guardar datos de una registro de variable.
Objetos de esta clase se guardan en la tabla de variables
name: nombre de la variable
type: tipo de la variable
address: direccion de memoria asignada a la variable
dimensions: dimensiones de la variable
"""
@dataclass
class VariableTableRecord:
    name: str
    type: VarType
    address: int = None
    dimensions: (int, int) = (1, 1)