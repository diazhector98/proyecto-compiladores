from virtual_machine.memory.block_type import BlockType

class VirtualMachineMemoryBlock:
    def __init__(self, start_address, size):
        partition_size = size // 4
        self.start_address = start_address
        self.int_partition = [None] * partition_size
        self.float_partition = [None] * partition_size
        self.char_partition = [None] * partition_size
        self.bool_partition = [None] * partition_size

    def write(self, address, value, block_type):
        if block_type == BlockType.GLOBAL:
            if address >= 0 and address < 1250:
                self.write_int_address(address, value)
            elif address >= 1250 and address < 2500:
                self.write_float_address(address - 1250, value)  
            elif address >= 2500 and address < 3750:
                self.write_char_address(address - 2500, value)
            elif address >= 3750 and address < 5000:
                self.write_bool_address(address - 3750, value)
            else: 
                raise Exception("La direccion global a la que se desea accesar es erronea.")

        elif block_type == BlockType.LOCAL:
            if address >= 5000 and address < 6250:
                self.write_int_address(address - 5000, value)
            elif address >= 6250 and address < 7500:
                self.write_float_address(address - 6250, value)  
            elif address >= 7500 and address < 8750:
                self.write_char_address(address - 7500, value)
            elif address >= 8750 and address < 10000:
                self.write_bool_address(address - 8750, value) 
            else: 
                raise Exception("La direccion local a la que se desea accesar es erronea.") 

        elif block_type == BlockType.TEMP:
            if address >= 10000 and address < 11250:
                self.write_int_address(address - 10000, value)
            elif address >= 11250 and address < 12500:
                self.write_float_address(address - 11250, value)  
            elif address >= 12500 and address < 13750:
                self.write_char_address(address - 12500, value)
            elif address >= 13750 and address < 15000:
                self.write_bool_address(address - 13750, value)  
            else: 
                ("La direccion temporal a la que se desea accesar es erronea.")
            
        elif block_type == BlockType.CONSTANTS:
            if address >= 15000 and address < 16250:
                self.write_int_address(address - 15000, value)
            elif address >= 16250 and address < 17500:
                self.write_float_address(address - 16250, value)  
            elif address >= 17500 and address < 18750:
                self.write_char_address(address - 17500, value)
            elif address >= 18750 and address <= 20000:
                self.write_bool_address(address - 18750, value)
            else: 
                raise Exception("La direccion de constante a la que se desea accesar es erronea.") 
        
        elif block_type == BlockType.POINTER:
            if address >= 20000 and address < 21250:
                self.write_int_address(address - 20000, value)
            elif address >= 21250 and address < 22500:
                self.write_float_address(address - 21250, value)  
            elif address >= 22500 and address < 23750:
                self.write_char_address(address - 22500, value)
            elif address >= 23750 and address <= 25000:
                self.write_bool_address(address - 23750, value)
            else: 
                raise Exception("La direccion de pointer que desea leer es erronea.") 

        else:
            raise Exception("La direccion de memoria: ", address, "no es valida.")

    
    def read(self, address, block_type):
        if block_type == BlockType.GLOBAL:
            if address >= 0 and address < 1250:
                return self.read_int_address(address)
            elif address >= 1250 and address < 2500:
                return self.read_float_address(address - 1250)  
            elif address >= 2500 and address < 3750:
                return self.read_char_address(address - 2500)
            elif address >= 3750 and address < 5000:
                return self.read_bool_address(address - 3750)
            else: 
                raise Exception("La direccion global que desea leer es erronea.")

        elif block_type == BlockType.LOCAL:
            if address >= 5000 and address < 6250:
                return self.read_int_address(address - 5000)
            elif address >= 6250 and address < 7500:
                return self.read_float_address(address - 6250)  
            elif address >= 7500 and address < 8750:
                return self.read_char_address(address - 7500)
            elif address >= 8750 and address < 10000:
                return self.read_bool_address(address - 8750) 
            else: 
                raise Exception("La direccion local que se desea leer es erronea.") 

        elif block_type == BlockType.TEMP:
            if address >= 10000 and address < 11250:
                return self.read_int_address(address - 10000)
            elif address >= 11250 and address < 12500:
                return self.read_float_address(address - 11250)  
            elif address >= 12500 and address < 13750:
                return self.read_char_address(address - 12500)
            elif address >= 13750 and address < 15000:
                return self.read_bool_address(address - 13750)  
            else: 
                raise Exception("La direccion temporal que desea leer es erronea.")
            
        elif block_type == BlockType.CONSTANTS:
            if address >= 15000 and address < 16250:
                return self.read_int_address(address - 15000)
            elif address >= 16250 and address < 17500:
                return self.read_float_address(address - 16250)  
            elif address >= 17500 and address < 18750:
                return self.read_char_address(address - 17500)
            elif address >= 18750 and address <= 20000:
                return self.read_bool_address(address - 18750)
            else: 
                raise Exception("La direccion de constante que desea leer es erronea.") 
            
        elif block_type == BlockType.POINTER:
            if address >= 20000 and address < 21250:
                return self.read_int_address(address - 20000)
            elif address >= 21250 and address < 22500:
                return self.read_float_address(address - 21250)  
            elif address >= 22500 and address < 23750:
                return self.read_char_address(address - 22500)
            elif address >= 23750 and address <= 25000:
                return self.read_bool_address(address - 23750)
            else: 
                raise Exception("La direccion de pointer que desea leer es erronea.") 
        
        else:
            raise Exception("La direccion de memoria: ", address, "no es valida.")


    def write_int_address(self, address, value):
        try:
            value = int(value)
            self.int_partition[address] = value
        except Exception:
            raise Exception("Value cannot be converted to int")

    def write_float_address(self, address, value):
        try:
            value = float(value)
            self.float_partition[address] = value
        except Exception:
            raise Exception("Value cannot be converted to float")

    def write_char_address(self, address, value):
        try:
            value = str(value)
            assert len(value) == 1
            self.char_partition[address] = value
        except Exception:
            raise Exception("Value cannot be converted to char")

    def write_bool_address(self, address, value):
        try:
            value = bool(value)
            self.bool_partition[address] = value
        except Exception:
            raise Exception("Value cannot be converted to bool")

    def read_int_address(self, address):
        return self.int_partition[address]

    def read_float_address(self, address):
        return self.float_partition[address]

    def read_char_address(self, address):
        return self.char_partition[address]

    def read_bool_address(self, address):
        return self.bool_partition[address]