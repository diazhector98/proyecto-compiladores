from dataclasses import dataclass
from virtual_machine.common.function import Function
from virtual_machine.memory.virtual_machine_memory_block import VirtualMachineMemoryBlock

@dataclass
class ActivationRecord:
    function: Function = None
    local_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(5000, 5000)
    temp_block: VirtualMachineMemoryBlock = VirtualMachineMemoryBlock(10000, 5000)
