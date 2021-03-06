
from compiler.semantic.memory.virtual_memory_block import VirtualMemoryBlock

"""
Clase para manejar la memoria virtual en el proceso de semántica.
Guarda los bloques de memoria para globales, locales, temporales y constantes
"""
class VirtualMemory:
    def __init__(self):
        memory_size = 25000
        self.block_size = memory_size // 5
        self.gloabl_block = VirtualMemoryBlock(0, self.block_size)
        self.local_block = VirtualMemoryBlock(self.block_size, self.block_size)
        self.temp_block = VirtualMemoryBlock(self.block_size * 2, self.block_size)
        self.constants_block = VirtualMemoryBlock(self.block_size * 3, self.block_size)
        self.pointers_block = VirtualMemoryBlock(self.block_size * 4, self.block_size)

    """
        Funciones para crear un dirección dependiendo 
        su tipo
            
        param address: tipo de variable 
        return: direccion creada segun su tipo
    """
    def create_global_address(self, type):
        return self.gloabl_block.create_address(type)

    def create_local_address(self, type, size=1):
        return self.local_block.create_address(type, size=size)

    def create_temporal_address(self, type):
        return self.temp_block.create_address(type)

    def create_constant_address(self, type):
        return self.constants_block.create_address(type)
    
    def create_pointer_address(self, type):
        return self.pointers_block.create_address(type)
    
    """
        Funcion para dar reset a la memoria local y temporal
        al terminar de procesar una funcion
    """
    def reset_local_and_temp_memory(self):
        self.local_block = VirtualMemoryBlock(self.block_size, self.block_size)
        self.temp_block = VirtualMemoryBlock(self.block_size * 2, self.block_size)

    """
        Funcion para obtener el tamaño del bloque para los apuntadores
    """
    def get_pointers_block_size(self):
        return self.pointers_block.int_partition.get_size()