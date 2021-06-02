from dataclasses import dataclass
from virtual_machine.common.function import Function
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock
from virtual_machine.memory.block_type import BlockType

"""
Esta clase representa una subrutina o scope de la pila de ejecución en la máquina virtual.
Almacena la función correspondiente, el índice actual en que esta su ejecución,
un bloque de memoria local y un bloque de memoria temporal.

"""
class ActivationRecord:
    function: Function = None
    current_quad_index: int = 0
    local_block: VirtualMachineMemoryBlock
    temp_block: VirtualMachineMemoryBlock

    def __init__(self, function=None, current_quad_index = 0):
        """
            Se inicializa esta clase con una variable objeto tipo funcion y el índice actual de ejecución.
            Por default, la función es nula y el índice es 0.
            En la inicialización se crean los bloques de memoria locales y temporales a partir
            de los tamaños especificados en el objeto de la función.
        """
        self.function = function
        self.current_quad_index = current_quad_index
        if function:
            self.local_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(
                5000, 
                5000,
                ints=function.local_var_int_size,
                floats=function.local_var_float_size,
                chars=function.local_var_char_size,
                bools=function.local_var_bool_size
                )
            self.temp_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(
                10000, 
                5000,
                ints=function.temp_var_int_size,
                floats=function.temp_var_float_size,
                chars=function.temp_var_char_size,
                bools=function.temp_var_bool_size
                )
            
        else:
            self.local_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(
                5000, 
                5000,
            )
            self.temp_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(10000, 5000)

    def write(self, address, value):
        """
        Función que escribe en la memoria local o temporal del ActivationRecord
        param address: argumento tipo entero correspondiendo a una dirección de memoria local/temporal
        param value: valor que se quiere escribir en memoria
        """
        if address >= 5000 and address < 10000:
                self.local_block.write(address, value, BlockType.LOCAL)
        elif address >= 10000 and address < 15000:
                self.temp_block.write(address, value, BlockType.TEMP)
