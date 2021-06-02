from virtual_machine.memory.block_type import BlockType
from virtual_machine.common.var_type import VarType

class VirtualMachineMemoryBlock:
    def __init__(self, start_address, size, ints=None, floats=None, chars=None, bools=None):
        partition_size = size // 4
        self.start_address = start_address
        
        ints_size = ints if ints != None else partition_size
        floats_size = floats if floats != None else partition_size
        chars_size = chars if chars != None else partition_size
        bools_size = bools if bools != None else partition_size
        
        self.int_partition = [None] * ints_size
        self.float_partition = [None] * floats_size
        self.char_partition = [None] * chars_size
        self.bool_partition = [None] * bools_size

    def write(self, address, value, block_type):
        (real_address, var_type) = self.get_real_address_and_type(address, block_type)
        if var_type == VarType.INT:
            self.write_int_address(real_address, value)
        elif var_type == VarType.FLOAT:
            self.write_float_address(real_address, value)  
        elif var_type == VarType.CHAR:
            self.write_char_address(real_address , value)
        elif var_type == VarType.BOOL:
            self.write_bool_address(real_address, value)
        else:
            raise Exception("Execution error: The memory address ", address, " trying to access in order to modify it in a memory block partition is invalid.")
    
    def read(self, address, block_type):
        (real_address, var_type) = self.get_real_address_and_type(address, block_type)
        if var_type == VarType.INT:
            return self.read_int_address(real_address)
        elif var_type == VarType.FLOAT:
            return self.read_float_address(real_address)
        elif var_type == VarType.CHAR:
            return self.read_char_address(real_address)
        elif var_type == VarType.BOOL:
            return self.read_bool_address(real_address)
        else:
            raise Exception("Execution error: The memory address ", address, " trying to access in order to read it in the memory block is invalid.")

    def write_int_address(self, address, value):
        try:
            value = int(value)
            self.int_partition[address] = value
        except Exception:
            raise Exception("Execution error: The integer value ", value, " trying to save in address ", address, " which corresponds to the integers memory block, can't be converted to integer.")

    def write_float_address(self, address, value):
        try:
            value = float(value)
            self.float_partition[address] = value
        except Exception:
            raise Exception("Execution error: The integer value ", value, " trying to save in address ", address, " which corresponds to the integers memory block, can't be converted to float.")

    def write_char_address(self, address, value):
        try:
            value = str(value)
            assert len(value) == 1
            self.char_partition[address] = value
        except Exception:
            raise Exception("Execution error: The integer value ", value, " trying to save in address ", address, " which corresponds to the integers memory block, can't be converted to char.")

    def write_bool_address(self, address, value):
        try:
            value = bool(value)
            self.bool_partition[address] = value
        except Exception:
            raise Exception("Execution error: The integer value ", value, " trying to save in address ", address, " which corresponds to the integers memory block, can't be converted to bool.")

    def read_int_address(self, address):
        return self.int_partition[address]

    def read_float_address(self, address):
        return self.float_partition[address]

    def read_char_address(self, address):
        return self.char_partition[address]

    def read_bool_address(self, address):
        return self.bool_partition[address]

    def get_real_address_and_type(self, address, block_type):
        if block_type == BlockType.GLOBAL:
            if address >= 0 and address < 1250:
                return address, VarType.INT
            elif address >= 1250 and address < 2500:
                return address - 1250 , VarType.FLOAT
            elif address >= 2500 and address < 3750:
                return address - 2500, VarType.CHAR
            elif address >= 3750 and address < 5000:
                return address - 3750, VarType.BOOL
            else: 
                raise Exception("Execution error: The memory address ", address, " trying to access to in order to modify in the global memory block is invalid.")

        elif block_type == BlockType.LOCAL:
            if address >= 5000 and address < 6250:
                return address - 5000, VarType.INT
            elif address >= 6250 and address < 7500:
                return address - 6250, VarType.FLOAT
            elif address >= 7500 and address < 8750:
                return address - 7500, VarType.CHAR
            elif address >= 8750 and address < 10000:
                return address - 8750, VarType.BOOL
            else: 
                raise Exception("Execution error: The memory address ", address, " trying to access in order to modify it in the local memory block is invalid.")

        elif block_type == BlockType.TEMP:
            if address >= 10000 and address < 11250:
                return address - 10000, VarType.INT
            elif address >= 11250 and address < 12500:
                return address - 11250, VarType.FLOAT
            elif address >= 12500 and address < 13750:
                return address - 12500, VarType.CHAR
            elif address >= 13750 and address < 15000:
                return address - 13750, VarType.BOOL
            else: 
                raise Exception("Execution error: The memory address ", address, " trying to access in order to modify it in the temporay memory block is invalid.")
            
        elif block_type == BlockType.CONSTANTS:
            if address >= 15000 and address < 16250:
                return address - 15000, VarType.INT
            elif address >= 16250 and address < 17500:
                return address - 16250, VarType.FLOAT
            elif address >= 17500 and address < 18750:
                return address - 17500, VarType.CHAR
            elif address >= 18750 and address <= 20000:
                return address - 18750, VarType.BOOL
            else: 
                raise Exception("Execution error: The memory address ", address, " trying to access in order to modify it in the constants memory block is invalid.") 
        
        elif block_type == BlockType.POINTER:
            if address >= 20000 and address < 25000:
                return address - 20000, VarType.INT
            else:
                raise Exception("Execution error: The memory address ", address, " trying to access in order to modify it in the pointers memory block is invalid.") 
        else:
            raise Exception("Execution error: The memory address ", address, " trying to access in order to read it in a memory block partition is invalid.")

    def print_sizes(self):
        print(
            "Ints:", len(self.int_partition), 
            "Floats", len(self.float_partition),
            "Chars", len(self.char_partition),
            "Bools", len(self.bool_partition)
        )