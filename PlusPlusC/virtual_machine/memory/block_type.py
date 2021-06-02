from enum import Enum

"""
    Clase Enum que contiene los 5 tipos de bloques de memoria de la máquina virtual
"""
class BlockType(Enum):
    GLOBAL = "GLOBAL"
    CONSTANTS = "CONSTANTS"
    LOCAL = "LOCAL"
    TEMP = "TEMP"
    POINTER = "POINTER"