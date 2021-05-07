import sys
sys.path.insert(0, '.')

from sly import Parser
from lexer import PlusPlusCLexer
from semantic_logic import SemanticHandler
from DirectorioFunciones import FuncReturnType, VarType

""" Falta while, for, hacer pruebas, eliminar recursividad """

class PlusPlusCParser(Parser):
    contains_error = False
    tokens = PlusPlusCLexer.tokens

    start = 'program'
    semantic_actions = SemanticHandler()

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        )

    def __init__(self):
        self.names = { }

    @_('inicio_programa ";" globals funciones main')
    def program(self, p):
        self.semantic_actions.print_quadruples()

    @_('PROGRAM ID')
    def inicio_programa(self, p):
        self.semantic_actions.initialize_program()

    @_('global_aux globals', 'epsilon')
    def globals(self, p):
        pass

    @_('GLOBALS ID tipo ";"')
    def global_aux(self, p):
        self.semantic_actions.set_variable(p.ID, VarType(p.tipo))
        pass
    
    @_('INT_TYPE', 'FLOAT_TYPE', 'CHAR_TYPE', 'BOOL_TYPE')
    def tipo(self, p):
        return p[0]

    @_('funcion', 'funcion funciones')
    def funciones(self, p):
        pass

    @_('declaracion_funcion bloque'
    )
    def funcion(self, p):
        self.semantic_actions.end_func()
        pass

    # TODO: Manejar funciones tipo void para manejo de funciones...(como la de arriba)
    @_(
    'FUNC ID "(" parametros ")" ARROW VOID bloque'
    )
    def funcion(self, p):
        self.semantic_actions.set_init_func(p.ID, FuncReturnType.VOID)
        self.semantic_actions.set_parametros(p.parametros)

    @_('FUNC ID "(" parametros ")" ARROW tipo')
    def declaracion_funcion(self, p):
        self.semantic_actions.set_init_func(p.ID, FuncReturnType(p.tipo))
        self.semantic_actions.set_parametros(p.parametros)
        pass

    @_('ID tipo')
    def parametros(self, p):
        return [(p[0], VarType(p.tipo))]

    @_('ID tipo "," parametros')
    def parametros(self, p):
        p.parametros.append((p[0], VarType(p.tipo)))
        return p.parametros

    @_('epsilon')
    def parametros(self, p):
        return []

    #Epsilon
    @_('')
    def epsilon(self, p):
        pass

    #Main
    @_('inicio_main bloque')
    def main(self, p):
        pass

    @_('MAIN "(" ")"')
    def inicio_main(self, p):
        self.semantic_actions.set_goto_main()

    #Bloque
    @_('"{" estatutos "}"', '"{" "}"')
    def bloque(self, p):
        pass

    @_('estatuto', 'estatuto estatutos')
    def estatutos(self, p):
        pass

    #Estatuto
    @_('escritura', 'lectura', 'retorno', 'asignacion', 'ciclo_while', 'condicion', 'declaracion_asignacion', 'llamada_funcion ";"')
    def estatuto(self, p):
        pass

    #Escritura
    @_('PRINT "(" constante ")" ";"')
    def escritura(self, p):
        self.semantic_actions.handle_print()
        pass

    @_('PRINT "(" ID ")" ";"')
    def escritura(self, p):
        self.semantic_actions.consume_operand(p.ID)
        self.semantic_actions.handle_print()
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
        self.semantic_actions.add_var_operand(p[0])
        pass

    #Declaracion
    @_('VAR ID tipo ";"')
    def declaracion_asignacion(self, p):
        self.semantic_actions.set_variable(p.ID, VarType(p.tipo))
        pass

    #Expresion
    @_('exp', 'llamada_funcion')
    def expresion(self, p):
        pass

    @_('exp operador_comparativo exp')
    def expresion(self, p):
        self.semantic_actions.set_quadruple()

    @_('termino')
    def exp(self, p):
        pass

    @_('termino operador_termino exp')
    def exp(self, p):
        self.semantic_actions.set_quadruple()

    @_('factor')
    def termino(self, p):
        pass

    @_('factor operador_factor termino')
    def termino(self, p):
        self.semantic_actions.set_quadruple()

    @_('"(" expresion ")"', 'operador_termino constante', 'constante')
    def factor(self, p):
        pass

    @_('ID')
    def factor(self, p):
        self.semantic_actions.consume_operand(p[0])

    @_('C_INTEGER')
    def constante(self, p):
        self.semantic_actions.consume_operand(p[0], VarType.INT)
        pass

    @_('C_FLOAT')
    def constante(self, p):
        self.semantic_actions.consume_operand(p[0], VarType.FLOAT)
        pass

    @_('C_CHAR')
    def constante(self, p):
        self.semantic_actions.consume_operand(p[0], VarType.CHAR)
        pass    

    @_('LT', 'GT', 'LTEQUAL', 'GTEQUAL', 'NOTEQUAL', 'EQUAL')
    def operador_comparativo(self, p):
        self.semantic_actions.consume_operator(p[0])
        pass
    
    @_('"+"', '"-"')
    def operador_termino(self, p):
        self.semantic_actions.consume_operator(p[0])
    
    @_('"*"', '"/"')
    def operador_factor(self, p):
        self.semantic_actions.consume_operator(p[0])

    #If
    @_('if_inicial bloque condicion_aux')
    def condicion(self, p):
        self.semantic_actions.set_end_of_if()
        pass

    @_('IF condiciones')
    def if_inicial(self, p):
        self.semantic_actions.set_initial_if()
        pass
    
    @_('else_inicial bloque', 'epsilon')
    def condicion_aux(self, p):
        pass

    @_('ELSE')
    def else_inicial(self, p):
        self.semantic_actions.set_else()
        pass

    #While
    @_('while_inicial bloque')
    def ciclo_while(self, p):
        self.semantic_actions.set_end_of_while()

    @_('WHILE condiciones')
    def while_inicial(self, p):
        self.semantic_actions.set_initial_while()

    @_('expresion', 'expresion operador_condicional condiciones')
    def condiciones(self, p):
        pass

    @_('AND', 'OR')
    def operador_condicional(self, p):
        pass

    #Llamadas a funciones
    @_('ID "(" argumentos_funcion ")"')
    def llamada_funcion(self, p):
        self.semantic_actions.set_function_call(p[0], p.argumentos_funcion)

    @_('argumento_funcion')
    def argumentos_funcion(self, p):
        return [p.argumento_funcion]

    @_('argumento_funcion "," argumentos_funcion')
    def argumentos_funcion(self, p):
        p.argumentos_funcion.append(p.argumento_funcion)
        return p.argumentos_funcion

    @_('epsilon')
    def argumentos_funcion(self, p):
        return []

    @_('exp')
    def argumento_funcion(self, p):
        argument = self.semantic_actions.stack.operands.pop()
        return argument

    def error(self, p):
        if p:
            print("Syntax error at token", p.type, p.value)
            self.contains_error = True

if __name__ == '__main__':
    parser = PlusPlusCParser()