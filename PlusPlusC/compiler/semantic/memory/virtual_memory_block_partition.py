
"""
Clase para manejar direcciones de un tipo de variables (e.g INT)

"""

class VirtualMemoryBlockPartition:
    def __init__(self, start_address, size):
        self.start_address = start_address
        self.current_address = start_address
        self.end_address = start_address + size

    def create_address(self):
        address = self.current_address
        self.current_address += 1
        return address
