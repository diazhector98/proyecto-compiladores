from dataclasses import dataclass
from virtual_machine.common.function import Function
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock
from virtual_machine.memory.block_type import BlockType

@dataclass
class ActivationRecord:
    function: Function = None
    current_quad_index: int = 0
    local_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(5000, 5000)
    temp_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(10000, 5000)

    def write(self, address, value):
        if address >= 5000 and address < 10000:
                self.local_block.write(address, value, BlockType.LOCAL)
        elif address >= 10000 and address < 15000:
                self.temp_block.write(address, value, BlockType.TEMP)
