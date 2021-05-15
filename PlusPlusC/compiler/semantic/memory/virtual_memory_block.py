from compiler.semantic.memory.virtual_memory_block_partition import VirtualMemoryBlockPartition
from compiler.semantic.common.DirectorioFunciones import VarType

"""
Clase para manejar un bloque de memoria (e.g globales)
"""

class VirtualMemoryBlock:
    def __init__(self, start_address, size):
        partition_size = size // 4
        self.start_address = start_address
        self.int_partition = VirtualMemoryBlockPartition(start_address, partition_size)
        self.float_partition = VirtualMemoryBlockPartition(start_address + partition_size, partition_size)
        self.char_partition = VirtualMemoryBlockPartition(start_address + partition_size * 2, partition_size)
        self.bool_partition = VirtualMemoryBlockPartition(start_address+ partition_size * 3, partition_size)

    def create_address(self, t):
        if t == VarType.INT:
            return self.create_int_address()
        if t == VarType.FLOAT:
            return self.create_float_address()
        if t == VarType.CHAR:
            return self.create_char_address()
        if t == VarType.BOOL:
            return self.create_bool_address()

    def create_int_address(self):
        return self.int_partition.create_address()

    def create_float_address(self):
        return self.float_partition.create_address()

    def create_char_address(self):
        return self.char_partition.create_address()

    def create_bool_address(self):
        return self.bool_partition.create_address()
