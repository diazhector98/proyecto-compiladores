from enum import Enum

class BlockType(Enum):
    GLOBAL = "GLOBAL"
    CONSTANTS = "CONSTANTS"
    LOCAL = "LOCAL"
    TEMP = "TEMP"