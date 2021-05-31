from dataclasses import dataclass
from virtual_machine.common.function import Function
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock
from virtual_machine.memory.block_type import BlockType

class ActivationRecord:
    function: Function = None
    current_quad_index: int = 0
    local_block: VirtualMachineMemoryBlock
    temp_block: VirtualMachineMemoryBlock

    def __init__(self, function=None, current_quad_index = 0):
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
        if address >= 5000 and address < 10000:
                self.local_block.write(address, value, BlockType.LOCAL)
        elif address >= 10000 and address < 15000:
                self.temp_block.write(address, value, BlockType.TEMP)
