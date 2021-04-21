from sly import Lexer

class PlusPlusCLexer(Lexer):
    
    #Lenguage tokens
    tokens = {

        ID,
        PROGRAM,
        MAIN,
        GLOBALS,

        #For variables
        VAR,

        # For variable types
        INT_TYPE,
        FLOAT_TYPE,
        CHAR_TYPE,

        # For constant variable values
        C_INTEGER,
        C_FLOAT,

        #For functions
        FUNC,
        RETURN,
        VOID,
        ARROW,

        #For Actions
        INPUT,
        PRINT,

        #For conditionals
        IF,
        ELSE,

        #For cycles
        WHILE,

        AND,
        OR,
        EQUAL,
        ASSIGN,
        NOTEQUAL,
        LTEQUAL,
        GTEQUAL,
        LT,
        GT
    }

    ignore = ' \t'
    ignore_comment = r'\#.*'
    literals = {'(', ')', '[', ']', 
                '{', '}', ';', ':', 
                ',', '+', '-', '*', 
                '/'}

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['if'] = IF
    ID['else'] = ELSE
    ID['print'] = PRINT
    ID['program'] = PROGRAM
    ID['globals'] = GLOBALS
    ID['var'] = VAR
    ID['int'] = INT_TYPE
    ID['float'] = FLOAT_TYPE
    ID['char'] = CHAR_TYPE
    ID['func'] = FUNC
    ID['main'] = MAIN
    ID['while'] = WHILE
    ID['input'] = INPUT
    ID['return'] = RETURN
    ID['void'] = VOID

    AND = r'&&'
    OR = r'\|\|'
    EQUAL = r'=='
    ASSIGN = r'='
    NOTEQUAL = r'!='
    LTEQUAL = r'<='
    GTEQUAL = r'>='
    LT = r'<'
    GT = r'>'
    ARROW = r'->'

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
      t.value = t.value
      return t
    
    @_(r'\d+')
    def C_INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\d+\.\d+')
    def C_FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\n+')
    def count_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Lexical error. Illegal character \" " + str(t.value[0]) + " \". Line #" + str(self.lineno) )
        self.index += 1

Tokens = PlusPlusCLexer.tokens

            