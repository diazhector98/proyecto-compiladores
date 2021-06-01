import sys
import os

sys.path.insert(0, '.')

from compiler.lexer.lexer import PlusPlusCLexer
from compiler.parser.parser import PlusPlusCParser

def get_absolute_path(path):
    if os.path.isabs(path):
        return path
    
    cwd = os.getcwd()
    file_path = os.path.join(cwd, path)
    return file_path


if __name__ == '__main__':

    arguments = sys.argv
    lexer = PlusPlusCLexer()
    parser = PlusPlusCParser()
    input_file_name = "tests/test_two.ppc"
    
    if len(arguments) == 2:
        # Input file specified but no output file specified
        input_file_name = arguments[1]
    elif len(arguments) == 3:
        # TODO: Specifiy output file
        input_file_name = arguments[1]

    input_abs_path = get_absolute_path(input_file_name)
    input_file = open(input_abs_path, "r")
    text = input_file.read()
    parser.parse(lexer.tokenize(text))
    compiler_output = parser.output