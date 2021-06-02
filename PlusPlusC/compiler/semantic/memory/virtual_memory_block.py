from compiler.semantic.memory.virtual_memory_block_partition import VirtualMemoryBlockPartition
from compiler.semantic.common.DirectorioFunciones import VarType

"""
Clase para manejar un bloque de memoria (e.g globales)
"""

class VirtualMemoryBlock:
    def __init__(self, start_address, size):
        partition_size = size // 4
        self.start_address = start_address
        self.int_partition = VirtualMemoryBlockPartition(start_address, partition_size - 1)
        self.float_partition = VirtualMemoryBlockPartition(start_address + partition_size, partition_size - 1)
        self.char_partition = VirtualMemoryBlockPartition(start_address + partition_size * 2, partition_size - 1)
        self.bool_partition = VirtualMemoryBlockPartition(start_address+ partition_size * 3, partition_size - 1)

    def create_address(self, t, size=1):
        """
            Función para crear un dirección de una particionn
            dependiendo su tipo. 

            param address: tipo de variable 
            return: direccion creada segun su tipo
        """
    
        if t == VarType.INT:
            return self.create_int_address(size)
        if t == VarType.FLOAT:
            return self.create_float_address(size)
        if t == VarType.CHAR:
            return self.create_char_address(size)
        if t == VarType.BOOL:
            return self.create_bool_address(size)

    def create_int_address(self, size=1):
        return self.int_partition.create_address(size=size)

    def create_float_address(self, size=1):
        return self.float_partition.create_address(size=size)

    def create_char_address(self, size=1):
        return self.char_partition.create_address(size=size)

    def create_bool_address(self, size=1):
        return self.bool_partition.create_address(size=size)
