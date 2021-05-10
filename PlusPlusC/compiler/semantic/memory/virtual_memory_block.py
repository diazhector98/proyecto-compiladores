from compiler.semantic.memory.virtual_memory_block_partition import VirtualMemoryBlockPartition
"""
Clase para manejar un bloque de memoria (e.g globales)
"""

class VirtualMemoryBlock:
    def __init__(self):
        self.int_partition = VirtualMemoryBlockPartition()
        self.float_partition = VirtualMemoryBlockPartition()
        self.char_partition = VirtualMemoryBlockPartition()
        self.bool_partition = VirtualMemoryBlockPartition()

    def create_address(self, t):
        if t == 'INT':
            self.create_int_address()
        if t == 'FLOAT':
            self.create_float_address()
        if t == 'CHAR':
            self.create_char_address()
        if t == 'BOOL':
            self.create_bool_address()

    def create_int_address():
        self.int_partition.create_address()

    def create_float_address():
        self.float_partition.create_address()

    def create_char_address():
        self.char_partition.create_address()

    def create_bool_address():
        self.bool_partition.create_address()
