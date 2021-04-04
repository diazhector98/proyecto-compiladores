import sys
sys.path.insert(0, '.')

from sly import Parser
from TeamPlusPlusLexer import TeamPlusPlusLexer

""" Falta while, for, hacer pruebas, eliminar recursividad """

class TeamPlusPlusParser(Parser):
    contains_error = False
    tokens = TeamPlusPlusLexer.tokens

    start = 'program'

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        )

    def __init__(self):
        self.names = { }

    @_('PROGRAM ID ";" funciones', 
      'PROGRAM ID ";" globals funciones main')
    def program(self, p):
        pass

    @_('GLOBALS declaraciones')
    def globals(self, p):
        pass

    @_('identificadores tipo ";"', 
      'identificadores tipo ";" declaraciones')
    def declaraciones(self, p):
        pass

    @_('ID', 'ID "," identificadores')
    def identificadores(self, p):
        pass

    @_('INT_TYPE', 'FLOAT_TYPE', 'CHAR_TYPE')
    def tipo(self, p):
        pass

    @_('funcion', 'funcion funciones')
    def funciones(self, p):
        pass

    @_('FUNC ID "(" parametros ")" ARROW tipo "{" "}"')
    def funcion(self, p):
        pass

    @_('ID tipo', 'ID tipo "," parametros')
    def parametros(self, p):
        pass

    @_('epsilon')
    def parametros(self, p):
        pass

    #Epsilon
    @_('')
    def epsilon(self, p):
        pass

    #Main
    @_('MAIN "(" ")" bloque')
    def main(self, p):
        pass

    #Bloque
    @_('"{" bloque2 "}"')
    def bloque(self, p):
        pass

    @_('epsilon', 'estatuto', 'estatuto bloque2')
    def bloque2(self, p):
        pass
    
    #Expresion
    @_('exp expresion2')
    def expresion(self, p):
        pass

    @_('expresion3 exp', 'epsilon')
    def expresion2(self, p):
        pass

    @_('LT', 'GT', 'LTEQUAL', 'GTEQUAL', 'NOTEQUAL', 'EQUAL')
    def expresion3(self, p):
        pass

    #Exp
    @_('termino exp2')
    def exp(self, p):
        pass

    @_('exp3 exp', 'epsilon')
    def exp2(self, p):
        pass
    
    @_('"+"', '"-"')
    def exp3(self, p):
        pass

    #Termino
    @_('factor termino2')
    def termino(self, p):
        pass

    @_('termino3 termino', 'epsilon')
    def termino2(self, p):
        pass
    
    @_('"*"', '"/"')
    def termino3(self, p):
        pass

    #Factor
    """Incomplete"""

    @_('"(" expresion ")"', 'epsilon')
    def factor(self, p):
        pass

    #Estatuto
    @_('asignacion', 'escritura', 'lectura', 'condicion')
    def estatuto(self, p):
        pass

    #Asignacion
    @_('ID ASSIGN expresion')
    def asignacion(self, p):
        pass

    #Escritura
    @_('PRINT "(" ID ")"')
    def escritura(self, p):
        pass

    #Lectura
    @_('INPUT "(" ID ")"')
    def lectura(self, p):
        pass

    #Condicion
    @_('IF expresionesCond bloque condicion2')
    def condicion(self, p):
        pass

    @_('expresion expresionesCond2')
    def expresionesCond(self, p):
        pass

    @_('AND expresionesCond', 'OR expresionesCond', 'epsilon')
    def expresionesCond2(self, p):
        pass

    @_('ELSE bloque', 'epsilon')
    def condicion2(self, p):
        pass

    

    #While

    #For


    def error(self, p):
        if p:
            print("Syntax error at token", p.type, p.value)
            self.contains_error = True

if __name__ == '__main__':
    parser = TeamPlusPlusParser()