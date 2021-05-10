
from compiler.semantic.memory.virtual_memory_block import VirtualMemoryBlock

class VirtualMemory:
    def __init__(self):
        self.gloabl_block = VirtualMemoryBlock()
        self.local_block = VirtualMemoryBlock()
        self.temp_block = VirtualMemoryBlock()
        self.constants_block = VirtualMemoryBlock()

    def create_global_address(self, type):
        self.gloabl_block.create_address(type)

    def create_local_address(self, type):
        self.local_block.create_address(type)

    def create_temporal_address(self, type):
        self.temp_block.create_address(type)

    def create_constant_address(self, type):
        self.constants_block.create_address(type)