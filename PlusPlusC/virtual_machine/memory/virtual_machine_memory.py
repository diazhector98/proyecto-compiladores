
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock
from virtual_machine.memory.block_type import BlockType
"""
Clase para manejar la memoria virtual en el proceso de semántica.
Guarda los bloques de memoria para globales, locales, temporales y constantes
"""
class VirtualMachineMemory:
    def __init__(self):
        memory_size = 20000
        self.block_size = memory_size // 4
        self.gloabl_block = VirtualMachineMemoryBlock(0, self.block_size)
        self.local_block = VirtualMachineMemoryBlock(self.block_size, self.block_size)
        self.temp_block = VirtualMachineMemoryBlock(self.block_size * 2, self.block_size)
        self.constants_block = VirtualMachineMemoryBlock(self.block_size * 3, self.block_size)

    def write(self, address, value):
        pass

    def read(self, address):
        pass

    def get_block_type(self, address):
        return BlockType.GLOBAL

    