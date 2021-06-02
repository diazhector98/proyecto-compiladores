"""
    Clase representando una función usada en los cuádruplos creados en compilación.
    Esta clase también es usada para almacenar información
    del scope global y del bloque main
"""

class Function:
    name: str
    start_quadruple_index: int = None
    temp_var_int_size: int = 0
    temp_var_float_size: int = 0
    temp_var_char_size: int = 0
    temp_var_bool_size: int = 0
    local_var_int_size: int = 0
    local_var_float_size: int = 0
    local_var_char_size: int = 0
    local_var_bool_size: int = 0

    def __init__(self, output_line):
        """
            De la salida de compilación, se obtiene una línea de la sección de funciones.
            Esta se divide y se procesan sus cuatro elementos

            param output_line: linea de la función de la salida de compilación
        """
        string_elements = output_line.split(' ')
        self.string_elements = [e for e in string_elements if e != '']
        self.process_string_elements()

    def process_string_elements(self):
        """
            Función que parsea los elementos de la línea de entrada para la clase:
            1. El nombre de la función
            2. El índice de inicio de la función
            3. Las cantidades de las variables temporales
            4. Las cantidades de las variables locales
        """
        [name, str_start_quadruple, str_temp_vars, str_local_vars] = self.string_elements

        self.name = name
        self.start_quadruple_index = int(str_start_quadruple)
        
        self.temp_vars = self.string_to_list(str_temp_vars)
        self.local_vars = self.string_to_list(str_local_vars)
        
        self.temp_var_int_size = self.temp_vars[0]
        self.temp_var_float_size = self.temp_vars[1]
        self.temp_var_char_size = self.temp_vars[2]
        self.temp_var_bool_size = self.temp_vars[3]
        
        self.local_var_int_size = self.local_vars[0]
        self.local_var_float_size = self.local_vars[1]
        self.local_var_char_size = self.local_vars[2]
        self.local_var_bool_size = self.local_vars[3]

    def string_to_list(self, string):
        """
            Función que convierte una variable string de formato "[int,int,int...]"
            a una lista de enteros

            param string: texto en formato "[int, int, ...]" representando 
            cantidad de variables utilizadas en la función
        """
        string = string.replace('[', '')
        string = string.replace(']', '')
        return list(map(int, string.split(',')))

    def __str__(self):
        """
            Método para imprimir de forma más legible información de la función. Usado
            para debugging.
        """
        return "{:<8} {:<4} {:<7} {:<7}".format(self.name, self.start_quadruple_index, str(self.temp_vars), str(self.local_vars))
