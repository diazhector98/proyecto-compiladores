from virtual_machine.common.quadruple import Quadruple

class FileReader:
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.text = self.file.read()
        self.process()

    def process(self):
        contents = self.text.split('%%')
        functions_text = contents[0]
        constants_text = contents[1]
        quadruples_text = contents[2]

        self.process_functions_text(functions_text)
        constants_table = self.process_constants_text(constants_text)
        self.process_quadruples_text(quadruples_text)
    
    def process_functions_text(self, text):
        lines = self.split_text(text)
        for l in lines:
            pass

    def process_constants_text(self, text):
        lines = self.split_text(text)
        table = dict()
        def process_line(line):
            [string_address, string_value] = line.split(' ')
            address = int(string_address)
            # TODO: Pensar en como determinar tipo de valor (por ahora convierte todos a float)
            value = float(string_value)
            table[address] = value

        for l in lines:
            process_line(l)
        
        return table

    def process_quadruples_text(self, text):
        lines = self.split_text(text)
        for l in lines:
            quadruple = Quadruple(l)
            print(quadruple)

    def split_text(self, text):
        lines = text.split('\n')
        lines = [line for line in lines if line != '']
        return lines
        
    