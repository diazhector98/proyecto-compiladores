import sys
sys.path.insert(0, '.')

from virtual_machine.file_reader import FileReader
from virtual_machine.virtual_machine import VirtualMachine

file_path = 'virtual_machine/test.txt'
virtual_machine = VirtualMachine(file_path)
