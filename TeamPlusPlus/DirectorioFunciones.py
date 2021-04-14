from dataclasses import dataclass


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
    return_type: str
    param_types: [str]

"""
Clase para guardar datos de una registro de variable.
Objetos de esta clase se guardan en la tabla de variables

name: nombre de la variable
type: tipo de la variable


"""
@dataclass
class VariableTableRecord:
    name: str
    type: str
