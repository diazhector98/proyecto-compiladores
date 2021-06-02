import sys
import os
sys.path.insert(0, '.')

from virtual_machine.file_reader import FileReader
from virtual_machine.virtual_machine import VirtualMachine
from virtual_machine import virtual_machine

def run_virtual_machine(file_result):
    virtual_machine = VirtualMachine(file_result, read_file=False, terminal=False)
    virtual_machine.run()
    virtual_machine_output = virtual_machine.output
    return virtual_machine_output

def get_absolute_path(path):
    if os.path.isabs(path):
        return path
    
    cwd = os.getcwd()
    file_path = os.path.join(cwd, path)
    return file_path

if __name__ == '__main__':
    arguments = sys.argv
    input_file_name = "output.txt"

    if len(arguments) == 2:
        input_file_name = arguments[1]
    
    input_abs_path = get_absolute_path(input_file_name)
    virtual_machine = VirtualMachine(input_abs_path)
    virtual_machine.run()