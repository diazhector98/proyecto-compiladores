from compiler.semantic.handler import SemanticHandler

class OutputGenerator:
    def __init__(self, semantic_handler: SemanticHandler, file_name=None):
        self.functions = semantic_handler.functions_directory
        self.constants = semantic_handler.constants_table
        self.quadruples = semantic_handler.quadruples
        self.number_of_pointers = semantic_handler.get_number_of_pointers_used()
        if file_name:
            self.file_name = file_name
        else:
            self.file_name = 'output.txt'

    def generate(self):
        f = open(self.file_name, "w")
        pointers_section = str(self.number_of_pointers) + "\n"
        functions_section = self.get_functions_section()
        constants_section = self.get_constants_section()
        quadruples_section = self.get_quadruples_section()
        separator = "%%\n"
        f.write(pointers_section)
        f.write(separator)
        f.write(functions_section)
        f.write(separator)
        f.write(constants_section)
        f.write(separator)
        f.write(quadruples_section)
        return pointers_section + separator + functions_section + separator + constants_section + separator + quadruples_section

    def get_functions_section(self) -> str:
        result = ""
        for function_name in self.functions:
            function = self.functions[function_name]
            result = result + str(function) + "\n"
        return result

    def get_constants_section(self) -> str:
        result = ""
        for constant in self.constants:
            address = self.constants[constant]
            result = result + str(address) + " " + str(constant) + "\n"
        return result

    def get_quadruples_section(self) -> str:
        result = ""
        for quad in self.quadruples:
            result = result + str(quad) + "\n"
        return result