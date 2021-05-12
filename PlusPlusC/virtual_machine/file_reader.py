

class FileReader:
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.contents = self.file.read()
        print(self.contents)
    