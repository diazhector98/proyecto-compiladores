import sys
sys.path.insert(0, '.')

from lexer import PlusPlusCLexer
from parser import PlusPlusCParser

if __name__ == '__main__':
    lexer = PlusPlusCLexer()
    parser = PlusPlusCParser()
    
    file_name = "test_two.ppc"
    input_file = open(file_name, "r")
    text = input_file.read()
    parser.parse(lexer.tokenize(text))