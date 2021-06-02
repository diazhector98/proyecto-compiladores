from virtual_machine.memory.block_type import BlockType
from virtual_machine.common.var_type import VarType

"""

Clase que representa un bloque de memoria real (por ejemplo, bloque de memoria global)
Esta clase contiene cuatro arreglos representando cada uno de los primitivos de PPC (ints, floats, chars y bools)

"""

class VirtualMachineMemoryBlock:
    def __init__(self, size, ints=None, floats=None, chars=None, bools=None):
        """
            En la inicialización se crean los arreglos en donde se almacenarán los valores de la memoria.

            param size: tamaños del bloque. Utilizado para obtener el tamaño default de cada partición
            param ints: número de espacios para enteros requeridos
            param floats: número de espacios para flotantes requeridos
            param chars: número de espacios para chars requeridos
            param bools: número de espacios para booleanos requeridos
        """
        partition_size = size // 4
        
        ints_size = ints if ints != None else partition_size
        floats_size = floats if floats != None else partition_size
        chars_size = chars if chars != None else partition_size
        bools_size = bools if bools != None else partition_size
        
        self.int_partition = [None] * ints_size
        self.float_partition = [None] * floats_size
        self.char_partition = [None] * chars_size
        self.bool_partition = [None] * bools_size

    def write(self, address, value, block_type):
        """
            Función que escribe en la memoria del bloque. Primero obtiene la 
            dirección real (índice de los arreglos) y el tipo de variable.

            param address: dirección virtual en donde se quiere escribir un valor
            param value: valor que se quiere escribir
            block_type: tipo de bloque que es este objeto, para facilitar la asignación del tipo de partición
        """
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
        """
            Función que lee en la memoria del bloque, despuñes de obtener la 
            dirección real (índice de los arreglos) y el tipo de variable

            param address: dirección virtual que se quiere leer
            param block_type: tipo de bloque que es este objeto, para facilitar la asignación del tipo de partición
        """
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

    def get_real_address_and_type(self, address, block_type):
        """
            Función que traduce la memoria virtual a un índice de los
            arreglos de la memoria.

            param address: dirección de la memoria virtual
            param block_type: tipo de bloque que es este objeto, para facilitar encontrar el tipo de variable

            return: (dirección real o índice de arreglo, tipo de variable)
        """
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
    
    """
        Las siguientes funciones sirven para escribir o leer de 
        particiones específicas del bloque de memoria.
    """

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