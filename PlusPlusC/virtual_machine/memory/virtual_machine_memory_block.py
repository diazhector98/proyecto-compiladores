class VirtualMachineMemoryBlock:
    def __init__(self, start_address, size):
        self.ints = []
        self.floats = []
        self.chars = []
        self.bools = []
