import sys
sys.path.insert(0, '.')

from virtual_machine.file_reader import FileReader
from virtual_machine.virtual_machine import VirtualMachine
from virtual_machine import virtual_machine

file_path = 'output.txt'
virtual_machine = VirtualMachine(file_path)
virtual_machine.run()
virtual_machine_output = virtual_machine.global_output_variable

def run_virtual_machine():
    file_path = 'output.txt'
    virtual_machine = VirtualMachine(file_path)
    virtual_machine.run()
    virtual_machine_output = virtual_machine.global_output_variable