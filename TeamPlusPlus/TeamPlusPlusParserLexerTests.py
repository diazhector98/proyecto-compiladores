import sys
sys.path.insert(0, '.')

from TeamPlusPlusLexer import TeamPlusPlusLexer
from TeamPlusPlusParser import TeamPlusPlusParser

if __name__ == '__main__':
    lexer = TeamPlusPlusLexer()
    parser = TeamPlusPlusParser()