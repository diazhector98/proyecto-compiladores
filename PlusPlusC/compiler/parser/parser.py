from sly import Parser
from compiler.lexer.lexer import PlusPlusCLexer
from compiler.semantic.handler import SemanticHandler
from compiler.semantic.generator import OutputGenerator
from compiler.semantic.common.DirectorioFunciones import FuncReturnType, VarType

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
        print("Cuádruplos")
        print("--------------")
        self.semantic_actions.print_quadruples()
        print("Globales")
        print("--------------")
        self.semantic_actions.print_globals_table()
        print("Constantes")
        print("--------------")
        self.semantic_actions.print_constants_table()
        output_generator = OutputGenerator(self.semantic_actions)
        output_generator.generate()

    @_('PROGRAM ID')
    def inicio_programa(self, p):
        self.semantic_actions.initialize_program()

    @_('global_aux globals', 'epsilon')
    def globals(self, p):
        pass

    @_('GLOBAL ID tipo ";"')
    def global_aux(self, p):
        self.semantic_actions.add_global(p.ID, VarType(p.tipo))
        pass
    
    @_('INT_TYPE', 'FLOAT_TYPE', 'CHAR_TYPE', 'BOOL_TYPE')
    def tipo(self, p):
        return p[0]

    @_('funcion', 'funcion funciones')
    def funciones(self, p):
        pass

    @_('declaracion_funcion bloque', 'declaracion_funcion_void bloque')
    def funcion(self, p):
        self.semantic_actions.end_func()
        pass

    @_('FUNC ID "(" parametros ")" ARROW tipo')
    def declaracion_funcion(self, p):
        self.semantic_actions.set_init_func(p.ID, FuncReturnType(p.tipo))
        self.semantic_actions.set_parametros(p.parametros)
        self.semantic_actions.add_global(p.ID, VarType(p.tipo))
        pass

    @_('FUNC ID "(" parametros ")" ARROW VOID')
    def declaracion_funcion_void(self, p):
        self.semantic_actions.set_init_func(p.ID, FuncReturnType.VOID)
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
    @_('escritura', 'lectura', 'retorno', 'asignacion', 'ciclo_while', 'condicion', 'declaracion', 'llamada_funcion ";"')
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
        self.semantic_actions.handle_read(p.ID)

    #Retorno
    @_('RETURN expresion ";"')
    def retorno(self, p):
        self.semantic_actions.handle_return()

    #Asignacion
    @_('asignacion_variable', 'asignacion_arreglo', 'asignacion_matrix')
    def asignacion(self, p):
        pass


    @_('ID ASSIGN expresion ";"')
    def asignacion_variable(self, p):
        self.semantic_actions.add_var_operand(p[0])
        pass

    @_('ID "[" exp "]" ASSIGN expresion ";"')
    def asignacion_arreglo(self, p):
        self.semantic_actions.handle_array_assign(p[0])
        pass

    @_('ID "[" exp "]" "[" exp "]" ASSIGN expresion ";"')
    def asignacion_matrix(self, p):
        self.semantic_actions.handle_matrix_assign(p[0])
        pass

    #Declaracion
    @_('declaracion_variable', 'declaracion_arreglo', 'declaracion_matriz')
    def declaracion(self, p):
        pass

    @_('VAR ID tipo ";"')
    def declaracion_variable(self, p):
        self.semantic_actions.set_variable(p.ID, VarType(p.tipo))

    @_('VAR ID "[" indice_arreglo "]" tipo ";"')
    def declaracion_arreglo(self, p):
        rows = p[3]
        self.semantic_actions.set_variable(p.ID, VarType(p.tipo), rows=rows)

    @_('VAR ID "[" indice_arreglo "]" "[" indice_arreglo "]" tipo ";"')
    def declaracion_matriz(self, p):
        rows = p[3]
        columns = p[6]
        self.semantic_actions.set_variable(p.ID, VarType(p.tipo), rows=rows, columns=columns)

    @_('C_INTEGER')
    def indice_arreglo(self, p):
        return p[0]

    #Expresion
    @_('exp')
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

    @_('llamada_funcion')
    def factor(self, p):
        pass

    @_('uso_arreglo')
    def factor(self, p):
        array_name = p.uso_arreglo[0]
        array_index = p.uso_arreglo[1]
        self.semantic_actions.consume_array_usage(array_name, array_index)

    @_('uso_matriz')
    def factor(self, p):
        matrix_name = p.uso_matriz[0]
        matrix_row_index = p.uso_matriz[1]
        matrix_column_index = p.uso_matriz[2]
        self.semantic_actions.consume_matrix_usage(matrix_name, (matrix_row_index, matrix_column_index))

    @_('ID "[" indice_uso_arreglo "]" ')
    def uso_arreglo(self, p):
        return (p.ID, p.indice_uso_arreglo)

    @_('ID "[" indice_uso_arreglo "]" "[" indice_uso_arreglo "]" ')
    def uso_matriz(self, p):
        return (p.ID, p[2], p[5])

    @_('exp')
    def indice_uso_arreglo(self, p):
        operando = self.semantic_actions.stack.operands.pop()
        tipo = self.semantic_actions.stack.types.pop()
        return (operando, tipo)

    @_('C_INTEGER')
    def constante(self, p):
        self.semantic_actions.consume_operand(p[0], VarType.INT, is_constant=True)

    @_('C_FLOAT')
    def constante(self, p):
        self.semantic_actions.consume_operand(p[0], VarType.FLOAT, is_constant=True)
        pass

    @_('C_CHAR')
    def constante(self, p):
        self.semantic_actions.consume_operand(p[0], VarType.CHAR, is_constant=True)
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
        argumento = self.semantic_actions.stack.operands.pop()
        tipo = self.semantic_actions.stack.types.pop()
        return (argumento, tipo)

    def error(self, p):
        if p:
            print("Syntax error at token", p.type, p.value)
            self.contains_error = True

if __name__ == '__main__':
    parser = PlusPlusCParser()