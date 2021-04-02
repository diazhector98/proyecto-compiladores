import sys
sys.path.insert(0, '.')

from sly import Parser
from TeamPlusPlusLexer import TeamPlusPlusLexer

class TeamPlusPlusParser(Parser):
    contains_error = False
    tokens = TeamPlusPlusLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', MULTIPLY, DIVIDE),
        )

    def __init__(self):
        self.names = { }

    @_('PROGRAM ID SEMICOLON')
    def program(self, p):
        pass

    def error(self, p):
        if p:
            print("Syntax error at token", p.type, p.value)
            self.contains_error = True
            self.errok()

if __name__ == '__main__':
    parser = TeamPlusPlusParser()