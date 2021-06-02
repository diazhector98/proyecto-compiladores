from virtual_machine.common.quadruple import Quadruple
from virtual_machine.common.function import Function

"""
Esta clase lee un archivo o una variable de texto y genera objetos de funciones, cuádruplos y constantes.
El método principal es el de process, que parsea el contenido de un texto
para facilitar el manejo de funciones y cuádruplos para la máquina virtual. Esto aparte ayuda
a que sea más sencillo establecer la memoria requerida por el programa PPC.

Se obtienen los atributos de la siguiente forma:

[pointers, functions, constants, constants_sizes, quadruples] = FileReader(input, read_file=read_file)

"""

class FileReader:
    def __init__(self, input, read_file=True):
        """
            param input: nombre de archivo o variable tipo string
            param read_file: establece si se quiere leer de un archivo o de una variable
        """
        if read_file:
            self.file = open(input, "r")
            self.text = self.file.read()
        else:
            self.text = input
        self.process()

    def process(self):
        """
            Función que separa el texto dado como input a partir de los delimitadores
            establecidos en compilación (%%)

            Establece cuatro elementos:
            1. Número de apuntadores necesarios del programa
            2. Directorio/Tabla de funciones
            3. Tabla de constantes y sus cantidades
            4. Lista de cuádruplos
        """
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
        """
            Función que regresa un diccionario de funciones a partir del bloque de funciones
            del archivo de compilación.
            param text: variable tipo string representando un bloque de definiciones de funciones
            return: diccionario con nombre de función como llave y valor como objeto de la función
        """
        lines = self.split_text(text)
        functions = [Function(l) for l in lines]
        functions_dictionary = {}
        for f in functions:
            functions_dictionary[f.name] = f
        return functions_dictionary

    def process_constants_text(self, text):
        """
            Función que regresa un diccionario de constantes
            param text: bloque de constantes de la salida de compilación
            return: diccionario con dirección de constante como llave y constante como valor
        """
        lines = self.split_text(text)
        table = dict()
        ints = 0
        floats = 0
        chars = 0
        bools = 0
        def process_line(line):
            """
                Función auxiliar que toma una linea del bloque de constantes
                y parsea su valor y dirección, guardandolos en el diccionario de constantes.
            """
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
        """
            param text: bloque de cuádruplos de salida de compilación
            return: lista de objetos de cuádruplos.
        """
        lines = self.split_text(text)
        quadruples = [Quadruple(l) for l in lines]
        return quadruples

    def split_text(self, text):
        """
            Función auxiliar que divide el texto por líneas y descarta texto vacío
            param text: parametro de tipo str
            return: lista de strings correspondiendo a cada línea del texto
        """
        lines = text.split('\n')
        lines = [line for line in lines if line != '']
        return lines

    def __iter__(self):
        """
            Función que ayuda a simplificar la forma en que se obtienen los atributos de esta clase:
            [pointers, functions, constants, constants_sizes, quadruples] = FileReader(input, read_file=read_file)
        """
        return iter((self.pointers, self.functions, self.constants_table,self.constants_sizes, self.quadruples))
        
    