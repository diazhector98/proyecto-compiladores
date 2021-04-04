from sly import Lexer

class TeamPlusPlusLexer(Lexer):
    
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

        # For variable values
        STRING,
        INTEGER,
        FLOAT,

        # Literals
        # LPAR,
        # RPAR,
        # LBRACKET,
        # RBRACKET,
        # PLUS,
        # MINUS,
        # MULTIPLY,
        # DIVIDE,
        # COLON,
        # SEMICOLON,
        # COMMA,

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
        FOR,
        TO,

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
    STRING = r'[a-zA-Z_][a-zA-Z0-9_]*'
    INTEGER = r'\d+'
    FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'

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
    ID['for'] = FOR
    ID['to'] = TO
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

    
    """Creo que podriamos poner en el parser algo asi @_('"+"') y omitirlos, ambas deben de funcionar
    #para que el parser sea más sencillo de leer """
    # Check This (literals...)
    # PLUS = r'\+'
    # MINUS = r'-'
    # MULTIPLY = r'\*'
    # DIVIDE = r'/'
    # LPAR = r'\('
    # RPAR = r'\)'
    # LBRACKET = r'{'
    # RBRACKET = r'}'
    # COLON = r':'
    # SEMICOLON = r';'
    # COMMA = r'\,'

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
      t.value = t.value
      return t
    
    @_(r'\n+')
    def count_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Lexical error. Illegal character \" " + str(t.value[0]) + " \". Line #" + str(self.lineno) )
        self.index += 1

Tokens = TeamPlusPlusLexer.tokens

            