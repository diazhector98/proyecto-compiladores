
from compiler.semantic.memory.virtual_memory_block import VirtualMemoryBlock

"""
Clase para manejar la memoria virtual en el proceso de semántica.
Guarda los bloques de memoria para globales, locales, temporales y constantes
"""
class VirtualMemory:
    def __init__(self):
        memory_size = 20000
        self.block_size = memory_size // 4
        self.gloabl_block = VirtualMemoryBlock(0, self.block_size)
        self.local_block = VirtualMemoryBlock(self.block_size, self.block_size)
        self.temp_block = VirtualMemoryBlock(self.block_size * 2, self.block_size)
        self.constants_block = VirtualMemoryBlock(self.block_size * 3, self.block_size)

    def create_global_address(self, type):
        return self.gloabl_block.create_address(type)

    def create_local_address(self, type):
        return self.local_block.create_address(type)

    def create_temporal_address(self, type):
        return self.temp_block.create_address(type)

    def create_constant_address(self, type):
        return self.constants_block.create_address(type)

    def reset_local_and_temp_memory(self):
        self.local_block = VirtualMemoryBlock(self.block_size, self.block_size)
        self.temp_block = VirtualMemoryBlock(self.block_size * 2, self.block_size)