
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
        string_elements = output_line.split(' ')
        self.string_elements = [e for e in string_elements if e != '']
        self.process_string_elements()

    def process_string_elements(self):
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
        string = string.replace('[', '')
        string = string.replace(']', '')
        return list(map(int, string.split(',')))

    def __str__(self):
        return "{:<8} {:<4} {:<7} {:<7}".format(self.name, self.start_quadruple_index, str(self.temp_vars), str(self.local_vars))
