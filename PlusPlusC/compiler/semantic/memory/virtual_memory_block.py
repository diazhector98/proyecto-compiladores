from compiler.semantic.memory.virtual_memory_block_partition import VirtualMemoryBlockPartition
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
        if t == 'INT':
            return self.create_int_address()
        if t == 'FLOAT':
            return self.create_float_address()
        if t == 'CHAR':
            return self.create_char_address()
        if t == 'BOOL':
            return self.create_bool_address()

    def create_int_address():
        return self.int_partition.create_address()

    def create_float_address():
        return self.float_partition.create_address()

    def create_char_address():
        return self.char_partition.create_address()

    def create_bool_address():
        return self.bool_partition.create_address()
