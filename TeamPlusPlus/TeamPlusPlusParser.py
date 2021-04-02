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

    @_('PROGRAM ID SEMICOLON funciones')
    def program(self, p):
        pass

    @_('PROGRAM ID SEMICOLON globals funciones')
    def program(self, p):
        pass

    @_('GLOBALS declaraciones')
    def globals(self, p):
        pass

    @_('identificadores tipo SEMICOLON')
    def declaraciones(self, p):
        pass

    @_('identificadores tipo SEMICOLON declaraciones')
    def declaraciones(self, p):
        pass

    @_('ID')
    def identificadores(self, p):
        pass

    @_('ID COMMA identificadores')
    def identificadores(self, p):
        pass

    @_('INT_TYPE')
    def tipo(self, p):
        pass

    @_('FLOAT_TYPE')
    def tipo(self, p):
        pass

    @_('funcion')
    def funciones(self, p):
        pass

    @_('funcion funciones')
    def funciones(self, p):
        pass

    @_('FUNC ID LPAR RPAR ARROW tipo LBRACKET RBRACKET')
    def funcion(self, p):
        pass

    def error(self, p):
        if p:
            print("Syntax error at token", p.type, p.value)
            self.contains_error = True

if __name__ == '__main__':
    parser = TeamPlusPlusParser()