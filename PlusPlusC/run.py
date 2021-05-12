import sys
sys.path.insert(0, '.')

from virtual_machine.file_reader import FileReader

file_path = 'virtual_machine/test.txt'
file_reader = FileReader(file_path)
