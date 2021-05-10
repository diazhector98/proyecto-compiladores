

class VirtualMemoryBlock:
    def __init__(self):
        pass

    def create_address(self, t):
        if t == 'INT':
            self.create_int_address()
        if t == 'FLOAT':
            self.create_float_address()
        if t == 'CHAR':
            self.create_char_address()
        if t == 'BOOL':
            self.create_bool_address()

    def create_int_address():
        pass

    def create_float_address():
        pass

    def create_char_address():
        pass

    def create_bool_address():
        pass
