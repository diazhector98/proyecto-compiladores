
"""
Clase para manejar direcciones de un tipo de variables (e.g INT)

"""

class VirtualMemoryBlockPartition:
    def __init__(self, start_address, size):
        self.start_address = start_address
        self.current_address = start_address
        self.end_address = start_address + size

    def create_address(self, size=1):
        address = self.current_address
        self.current_address += size
        return address
    
    def get_size(self):
        return self.current_address - self.start_address
