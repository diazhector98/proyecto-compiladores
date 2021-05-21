
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock
from virtual_machine.memory.block_type import BlockType
"""
Clase para manejar la memoria virtual en el proceso de semántica.
Guarda los bloques de memoria para globales, locales, temporales y constantes
"""
class VirtualMachineMemory:
    def __init__(self, constants):
        memory_size = 20000
        self.block_size = memory_size // 4
        self.gloabl_block = VirtualMachineMemoryBlock(0, self.block_size - 1)
        self.local_block = VirtualMachineMemoryBlock(self.block_size, self.block_size - 1)
        self.temp_block = VirtualMachineMemoryBlock(self.block_size * 2, self.block_size - 1)
        self.constants_block = VirtualMachineMemoryBlock(self.block_size * 3, self.block_size)

        # Escribiendo constantes a bloque de constantes
        for address in constants:
                value = constants[address]
                block_type = self.get_block_type(address)
                self.constants_block.write(address, value, block_type)

    def write(self, address, value):
        block_type = self.get_block_type(address)
        if address >= 0 and address < 5000:
                self.gloabl_block.write(address, value, block_type)
        elif address >= 5000 and address < 10000:
                self.local_block.write(address, value, block_type)
        elif address >= 10000 and address < 15000:
                self.temp_block.write(address, value, block_type)
        elif address >= 15000 and address <= 20000:
                self.constants_block.write(address, value, block_type)
        else:
            print("La direccion de memoria: ", address, "es invalida. No se puede acceder para modificar el valor en ella.")

    def read(self, address):
        block_type = self.get_block_type(address)
        if address >= 0 and address < 5000:
                return self.gloabl_block.read(address, block_type)
        elif address >= 5000 and address < 10000:
                return self.local_block.read(address, block_type)
        elif address >= 10000 and address < 15000:
                return self.temp_block.read(address, block_type)
        elif address >= 15000 and address <= 20000:
                return self.constants_block.read(address, block_type)
        else:
            print("La direccion de memoria: ", address, "es invalida. No se puede leer el valor guardado en ella.")

    def get_block_type(self, address):
        if address >= 0 and address < 5000:
                return BlockType.GLOBAL
        elif address >= 5000 and address < 10000:
                return BlockType.LOCAL
        elif address >= 10000 and address < 15000:
                return BlockType.TEMP
        elif address >= 15000 and address <= 20000:
                return BlockType.CONSTANTS
        else:
            print("La direccion de memoria: ", address, "es invalida.")
    