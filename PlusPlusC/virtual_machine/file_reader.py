from virtual_machine.common.quadruple import Quadruple
from virtual_machine.common.function import Function

class FileReader:
    def __init__(self, input, read_file=True):
        if read_file:
            self.file = open(input, "r")
            self.text = self.file.read()
        else:
            self.text = input
        self.process()

    def process(self):
        contents = self.text.split('%%')
        pointers_text = contents[0]
        functions_text = contents[1]
        constants_text = contents[2]
        quadruples_text = contents[3]
        
        self.pointers = int(pointers_text)
        self.functions = self.process_functions_text(functions_text)
        (self.constants_table, self.constants_sizes) = self.process_constants_text(constants_text)
        self.quadruples = self.process_quadruples_text(quadruples_text)
    
    def process_functions_text(self, text):
        lines = self.split_text(text)
        functions = [Function(l) for l in lines]
        functions_dictionary = {}
        for f in functions:
            functions_dictionary[f.name] = f
        return functions_dictionary

    def process_constants_text(self, text):
        lines = self.split_text(text)
        table = dict()
        ints = 0
        floats = 0
        chars = 0
        bools = 0
        def process_line(line):
            [string_address, string_value] = line.split(' ')
            address = int(string_address)
            constant_type = int
            
            if address >= 15000 and address < 16250:
                value = int(string_value)
            elif address >= 1650 and address < 17500:
                value = float(string_value)
                constant_type = float
            elif address >= 17500 and address < 18750:
                value = str(string_value)
                constant_type = str
            elif address >= 18750 and address <= 20000:
                value = bool(string_value)
                constant_type = bool
            else:
                raise Exception("Execution error: The constant memory address: ", string_address, "’, which corresponds to value: ", value, " it’s not valid. ")

            table[address] = value
            return constant_type

        for l in lines:
            constant_type = process_line(l)
            if constant_type == int:
                ints += 1
            if constant_type == float:
                floats += 1
            if constant_type == str:
                chars += 1
            if constant_type == bool:
                bools += 1
        return (table, [ints, floats, chars, bools])

    def process_quadruples_text(self, text):
        lines = self.split_text(text)
        quadruples = [Quadruple(l) for l in lines]
        return quadruples

    def split_text(self, text):
        lines = text.split('\n')
        lines = [line for line in lines if line != '']
        return lines

    def __iter__(self):
        return iter((self.pointers, self.functions, self.constants_table,self.constants_sizes, self.quadruples))
        
    