import sys
import os
sys.path.insert(0, '.')

from virtual_machine.file_reader import FileReader
from virtual_machine.virtual_machine import VirtualMachine
from virtual_machine import virtual_machine


cwd = os.getcwd()
file_path = os.path.join(cwd, 'PlusPlusC/output.txt')
print(file_path)
virtual_machine = VirtualMachine(file_path)
virtual_machine.run()

def run_virtual_machine(file_result):
    virtual_machine = VirtualMachine(file_result, read_file=False, terminal=False)
    virtual_machine.run()
    virtual_machine_output = virtual_machine.global_output_variable
    return virtual_machine_output