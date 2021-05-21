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
                self.write_float_address(address, value)  
            elif address >= 2500 and address < 3750:
                self.write_char_address(address, value)
            elif address >= 3750 and address < 5000:
                self.write_bool_address(address, value)
            else: 
                print("La direccion global a la que se desea accesar es erronea.")

        elif block_type == BlockType.LOCAL:
            if address >= 5000 and address < 6250:
                self.write_int_address(address, value)
            elif address >= 6250 and address < 7500:
                self.write_float_address(address, value)  
            elif address >= 7500 and address < 8750:
                self.write_char_address(address, value)
            elif address >= 8750 and address < 10000:
                self.write_bool_address(address, value) 
            else: 
                print("La direccion local a la que se desea accesar es erronea.") 

        elif block_type == BlockType.TEMP:
            if address >= 10000 and address < 11250:
                self.write_int_address(address, value)
            elif address >= 12250 and address < 13500:
                self.write_float_address(address, value)  
            elif address >= 13500 and address < 14750:
                self.write_char_address(address, value)
            elif address >= 14750 and address < 15000:
                self.write_bool_address(address, value)  
            else: 
                print("La direccion temporal a la que se desea accesar es erronea.")
            
        elif block_type == BlockType.CONSTANTS:
            if address >= 15000 and address < 16250:
                self.write_int_address(address, value)
            elif address >= 16250 and address < 17500:
                self.write_float_address(address, value)  
            elif address >= 17500 and address < 18750:
                self.write_char_address(address, value)
            elif address >= 18750 and address <= 20000:
                self.write_bool_address(address, value)
            else: 
                print("La direccion de constante a la que se desea accesar es erronea.") 
        
        else:
            print("La direccion de memoria: ", address, "no es valida.")

    
    def read(self, address, block_type):
        if block_type == BlockType.GLOBAL:
            if address >= 0 and address < 1250:
                self.read_int_address(address)
            elif address >= 1250 and address < 2500:
                self.read_float_address(address)  
            elif address >= 2500 and address < 3750:
                self.read_char_address(address)
            elif address >= 3750 and address < 5000:
                self.read_bool_address(address)
            else: 
                print("La direccion global que desea leer es erronea.")

        elif block_type == BlockType.LOCAL:
            if address >= 5000 and address < 6250:
                self.read_int_address(address)
            elif address >= 6250 and address < 7500:
                self.read_float_address(address)  
            elif address >= 7500 and address < 8750:
                self.read_char_address(address)
            elif address >= 8750 and address < 10000:
                self.read_bool_address(address) 
            else: 
                print("La direccion local que se desea leer es erronea.") 

        elif block_type == BlockType.TEMP:
            if address >= 10000 and address < 11250:
                self.read_int_address(address)
            elif address >= 12250 and address < 13500:
                self.read_float_address(address)  
            elif address >= 13500 and address < 14750:
                self.read_char_address(address)
            elif address >= 14750 and address < 15000:
                self.read_bool_address(address)  
            else: 
                print("La direccion temporal que desea leer es erronea.")
            
        elif block_type == BlockType.CONSTANTS:
            if address >= 15000 and address < 16250:
                self.read_int_address(address)
            elif address >= 16250 and address < 17500:
                self.read_float_address(address)  
            elif address >= 17500 and address < 18750:
                self.read_char_address(address)
            elif address >= 18750 and address <= 20000:
                self.read_bool_address(address)
            else: 
                print("La direccion de constante que desea leer es erronea.") 
        
        else:
            print("La direccion de memoria: ", address, "no es valida.")


    def write_int_address(self, address, value):
        self.int_partition[address] = value

    def write_float_address(self, address, value):
        self.float_partition[address] = value

    def write_char_address(self, address, value):
        self.char_partition[address] = value

    def write_bool_address(self, address, value):
        self.bool_partition[address] = value

    def read_int_address(self, address):
        return self.int_partition[address]

    def read_float_address(self, address):
        return self.float_partition[address]

    def read_char_address(self, address):
        return self.char_partition[address]

    def read_bool_address(self, address):
        return self.bool_partition[address]