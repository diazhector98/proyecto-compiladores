from compiler.semantic.handler import SemanticHandler

class OutputGenerator:
    def __init__(self, semantic_handler: SemanticHandler):
        self.functions = semantic_handler.functions_directory
        self.constants = semantic_handler.constants_table
        self.quadruples = semantic_handler.quadruples

    def generate(self):
        f = open("output.txt", "w")
        functions_section = self.get_functions_section()
        constants_section = self.get_constants_section()
        quadruples_section = self.get_quadruples_section()
        separator = "%%\n"
        f.write(functions_section)
        f.write(separator)
        f.write(constants_section)
        f.write(separator)
        f.write(quadruples_section)
        return functions_section + separator + constants_section + separator + quadruples_section

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