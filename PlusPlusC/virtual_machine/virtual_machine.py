from virtual_machine.file_reader import FileReader

class VirtualMachine:
    def __init__(self, filename):
        [functions, constants, quadruples] = FileReader(filename)