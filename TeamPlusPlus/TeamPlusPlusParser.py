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

    @_('PROGRAM ID SEMICOLON bloque')
    def program(self, p):
        pass

    @_('PROGRAM ID SEMICOLON vars bloque')
    def program(self, p):
        pass

    @_('VAR declaraciones')
    def vars(self, p):
        pass

    @_('identificadores COLON tipo SEMICOLON')
    def declaraciones(self, p):
        pass

    @_('identificadores COLON tipo SEMICOLON declaraciones')
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
    
    @_('LBRACKET estatutos RBRACKET')
    def bloque(self, p):
        pass

    @_('estatuto')
    def estatutos(self, p):
        pass

    @_('estatuto estatutos')
    def estatutos(self, p):
        pass
    
    @_('asignacion')
    def estatuto(self, p):
        pass

    @_('condicion')
    def estatuto(self, p):
        pass

    @_('escritura')
    def estatuto(self, p):
        pass

    @_('PRINT LPAR expresionesystrings RPAR SEMICOLON')
    def escritura(self, p):
        pass

    @_('expresion')
    def expresionesystrings(self, p):
        pass

    @_('STRING')
    def expresionesystrings(self, p):
        pass

    @_('expresion COMMA expresionesystrings')
    def expresionesystrings(self, p):
        pass

    @_('STRING COMMA expresionesystrings')
    def expresionesystrings(self, p):
        pass

    @_('IF LPAR expresion RPAR bloque SEMICOLON')
    def condicion(self,p):
        pass

    @_('IF LPAR expresion RPAR bloque ELSE bloque SEMICOLON')
    def condicion(self,p):
        pass

    @_('ID ASSIGN expresion SEMICOLON ')
    def asignacion(self, p):
        pass

    @_('exp')
    def expresion(self, p):
        pass

    @_('exp GT exp')
    def expresion(self, p):
        pass

    @_('exp LT exp')
    def expresion(self, p):
        pass

    @_('exp NOTEQUAL exp')
    def expresion(self, p):
        pass

    @_('termino')
    def exp(self, p):
        pass
    
    @_('termino opsplusminus exp')
    def exp(self, p):
        pass

    @_('factor')
    def termino(self, p):
        pass

    @_('factor opsfactores termino')
    def termino(self, p):
        pass

    @_('MULTIPLY')
    def opsfactores(self, p):
        pass

    @_('DIVIDE')
    def opsfactores(self, p):
        pass

    @_('LPAR expresion RPAR')
    def factor(self, p):
        pass

    @_('opsplusminus varcte')
    def factor(self, p):
        pass

    @_('varcte')
    def factor(self, p):
        pass

    @_('ID')
    def varcte(self, p):
        pass

    @_('INTEGER')
    def varcte(self, p):
        pass

    @_('FLOAT')
    def varcte(self, p):
        pass

    @_('PLUS')
    def opsplusminus(self, p):
        pass

    @_('MINUS')
    def opsplusminus(self, p):
        pass

    def error(self, p):
        if p:
            self.contains_error = True
            self.errok()

if __name__ == '__main__':
    parser = TeamPlusPlusParser()