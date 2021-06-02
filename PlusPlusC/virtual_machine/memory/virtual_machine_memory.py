
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock
from virtual_machine.memory.block_type import BlockType
"""
Clase para manejar la memoria virtual en el proceso de semántica.
Guarda los bloques de memoria para globales, locales, temporales y constantes
La memoria local y temporal se guarda en un objeto de tipo ActivationRecord
"""
class VirtualMachineMemory:
    def __init__(self, pointers, global_function, constants,constants_sizes, activation_record):
        """
                En la inicialización se especifíca el tamaño de memoria y el tamaño de cada bloque.
                Estos valores son utilizados para proveer un default. En realidad, el tamaño de los bloques
                es determinado en compilación.

                param pointers: número de apuntadores requeridos
                param global_function: objeto tipo Function para especificar el tamaño requerido de la memoria global
                param constants: diccionario de constantes
                param constants_sizes: cantidad de constantes para especificar el tamaño requerido de la memoria constante
                param activation_record: objeto tipo ActivationRecord que guarda la memoria local y temporal.
        """
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
        self.pointers_block = VirtualMachineMemoryBlock(
                self.block_size * 4, 
                self.block_size, 
                ints=pointers, 
                floats=0,
                chars=0,
                bools=0
        )
        # Guarda memoria local y temporal
        self.activation_record = activation_record
        # Escribiendo constantes a bloque de constantes
        for address in constants:
                value = constants[address]
                block_type = self.get_block_type(address)
                self.constants_block.write(address, value, block_type)

    def write(self, address, value):
        """
                Función para escribir un valor en la memoria. Primero,
                se obtiene el tipo de bloque en donde se quiere escribir.

                param address: dirección donde se quiere escribir un valor
                param value: valor que se quiere escribir
        """
        block_type = self.get_block_type(address)
        if block_type == BlockType.GLOBAL:
                self.gloabl_block.write(address, value, block_type)
        elif block_type == BlockType.LOCAL:
                self.activation_record.local_block.write(address, value, block_type)
        elif block_type == BlockType.TEMP:
                self.activation_record.temp_block.write(address, value, block_type)
        elif block_type == BlockType.CONSTANTS:
                self.constants_block.write(address, value, block_type)
        elif block_type == BlockType.POINTER:
                self.pointers_block.write(address, value, block_type)
        else:
            raise Exception("The memory address ", address, " is invalid. Can’t access it to modify its value.")

    def read(self, address):
        """
                Función para leer algún valor de memoria. Primero,
                se obtiene el bloque de memoria requerido a partir de su dirección.
                Si es un apuntador, se regresa el valor guardado en la casilla a la que apunta
                el apuntador (por lo que se hacen dos lecturas de memoria).
                
                param address: dirección de memoria
                return: valor guardado en espacio de memoria
        """
        block_type = self.get_block_type(address)

        if block_type == BlockType.GLOBAL:
                return self.gloabl_block.read(address, block_type)
        elif block_type == BlockType.LOCAL:
                return self.activation_record.local_block.read(address, block_type)
        elif block_type == BlockType.TEMP:
                return self.activation_record.temp_block.read(address, block_type)
        elif block_type == BlockType.CONSTANTS:
                return self.constants_block.read(address, block_type)
        elif block_type == BlockType.POINTER:
                address_saved_in_pointer = self.pointers_block.read(address, block_type)
                return self.read(address_saved_in_pointer)
        else:
            raise Exception("The memory address ", address, " is invalid. Can’t access it to read its value.")

    def get_block_type(self, address):
        """
                Función que regresa el tipo de bloque de memoria en donde se encuentra una dirección

                param address: dirección de memoria
                return: tipo de bloque de memoria de tipo BlockType
        """
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
            raise Exception("The memory address ", address, " is invalid.")
    