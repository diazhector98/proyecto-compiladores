import sys
sys.path.insert(0, '.')

from TeamPlusPlusLexer import TeamPlusPlusLexer
from TeamPlusPlusParser import TeamPlusPlusParser

if __name__ == '__main__':
    lexer = TeamPlusPlusLexer()
    parser = TeamPlusPlusParser()
    
    file_name = "test.ppc"
    input_file = open(file_name, "r")
    text = input_file.read()
    parser.parse(lexer.tokenize(text))