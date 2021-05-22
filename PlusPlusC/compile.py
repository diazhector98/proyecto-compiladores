import sys
sys.path.insert(0, '.')

from compiler.lexer.lexer import PlusPlusCLexer
from compiler.parser.parser import PlusPlusCParser

if __name__ == '__main__':
    lexer = PlusPlusCLexer()
    parser = PlusPlusCParser()
    
    file_name = "tests/test_eight.ppc"
    input_file = open(file_name, "r")
    text = input_file.read()
    parser.parse(lexer.tokenize(text))