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

    @_('FUNC ID "(" parametros ")" ARROW tipo bloque')
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
    @_('"{" estatutos "}"', '"{" "}"')
    def bloque(self, p):
        pass

    @_('estatuto', 'estatuto estatutos')
    def estatutos(self, p):
        pass

    #Estatuto
    @_('escritura', 'lectura', 'retorno', 'asignacion', 'ciclo_while', 'condicion')
    def estatuto(self, p):
        pass

    #Escritura
    @_('PRINT "(" ID ")" ";"')
    def escritura(self, p):
        pass

    #Lectura
    @_('INPUT "(" ID ")" ";"')
    def lectura(self, p):
        pass

    #Retorno
    @_('RETURN expresion ";"')
    def retorno(self, p):
        pass

    #Asignacion
    @_('ID ASSIGN expresion ";"')
    def asignacion(self, p):
        pass

    #Expresion
    @_('exp', 'exp operador_comparativo exp')
    def expresion(self, p):
        pass

    @_('termino', 'termino operador_termino exp')
    def exp(self, p):
        pass

    @_('factor', 'factor operador_factor termino')
    def termino(self, p):
        pass

    @_('"(" expresion ")"', 'operador_termino constante', 'constante', 'ID')
    def factor(self, p):
        pass

    @_('INTEGER', 'FLOAT')
    def constante(self, p):
        pass

    @_('LT', 'GT', 'LTEQUAL', 'GTEQUAL', 'NOTEQUAL', 'EQUAL')
    def operador_comparativo(self, p):
        pass
    
    @_('"+"', '"-"')
    def operador_termino(self, p):
        pass
    
    @_('"*"', '"/"')
    def operador_factor(self, p):
        pass

    #If
    @_('IF expresion bloque', 'IF expresion bloque ELSE bloque')
    def condicion(self, p):
        pass

    #While
    @_('WHILE expresion bloque')
    def ciclo_while(self, p):
        pass

    #For

    def error(self, p):
        if p:
            print("Syntax error at token", p.type, p.value)
            self.contains_error = True

if __name__ == '__main__':
    parser = TeamPlusPlusParser()