
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock
from virtual_machine.memory.block_type import BlockType
"""
Clase para manejar la memoria virtual en el proceso de semántica.
Guarda los bloques de memoria para globales, locales, temporales y constantes
"""
class VirtualMachineMemory:
    def __init__(self, global_function, constants,constants_sizes, activation_record):
        memory_size = 25000
        self.block_size = memory_size // 5        
        self.gloabl_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(
                0, 
                self.block_size,
                ints=global_function.local_var_int_size,
                floats=global_function.local_var_float_size,
                chars=global_function.local_var_char_size,
                bools=global_function.local_var_bool_size
        )

        self.constants_block = VirtualMachineMemoryBlock(
                self.block_size * 3, 
                self.block_size,
                ints=constants_sizes[0],
                floats=constants_sizes[1],
                chars=constants_sizes[2],
                bools=constants_sizes[3]
        )
        self.pointers_block = VirtualMachineMemoryBlock(self.block_size * 4, self.block_size)
        # Guarda memoria local y temporal
        self.activation_record = activation_record
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
                self.activation_record.local_block.write(address, value, block_type)
        elif address >= 10000 and address < 15000:
                self.activation_record.temp_block.write(address, value, block_type)
        elif address >= 15000 and address < 20000:
                self.constants_block.write(address, value, block_type)
        elif address >= 20000 and address < 25000:
                self.pointers_block.write(address, value, block_type)
        else:
            raise Exception("La direccion de memoria: ", address, "es invalida. No se puede acceder para modificar el valor en ella.")

    def read(self, address):
        block_type = self.get_block_type(address)
        if address >= 0 and address < 5000:
                return self.gloabl_block.read(address, block_type)
        elif address >= 5000 and address < 10000:
                return self.activation_record.local_block.read(address, block_type)
        elif address >= 10000 and address < 15000:
                return self.activation_record.temp_block.read(address, block_type)
        elif address >= 15000 and address < 20000:
                return self.constants_block.read(address, block_type)
        elif address >= 20000 and address <= 25000:
                address_saved_in_pointer = self.pointers_block.read(address, block_type)
                return self.read(address_saved_in_pointer)
        else:
            raise Exception("La direccion de memoria: ", address, "es invalida. No se puede leer el valor guardado en ella.")

    def get_block_type(self, address):
        if address >= 0 and address < 5000:
                return BlockType.GLOBAL
        elif address >= 5000 and address < 10000:
                return BlockType.LOCAL
        elif address >= 10000 and address < 15000:
                return BlockType.TEMP
        elif address >= 15000 and address < 20000:
                return BlockType.CONSTANTS
        elif address >= 20000 and address <= 25000:
                return BlockType.POINTER
        else:
            raise Exception("La direccion de memoria: ", address, "es invalida.")
    