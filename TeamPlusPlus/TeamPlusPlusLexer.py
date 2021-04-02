from sly import Lexer

class TeamPlusPlusLexer(Lexer):
    
    #Lenguage tokens
    tokens = {

        ID,
        PROGRAM,
        MAIN,

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
        LPAR,
        RPAR,
        LBRACKET,
        RBRACKET,
        PLUS,
        MINUS,
        MULTIPLY,
        DIVIDE,
        COLON,
        SEMICOLON,
        COMMA,

        #For functions
        FUNC,
        RETURN,
        VOID,

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

    ID['if'] = IF
    ID['else'] = ELSE
    ID['print'] = PRINT
    ID['program'] = PROGRAM
    ID['var'] = VAR
    ID['int'] = INT_TYPE
    ID['float'] = FLOAT_TYPE


    STRING = r'[a-zA-Z_][a-zA-Z0-9_]*'
    INTEGER = r'\d+'
    FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
    PROGRAM = r'program'
    MAIN = r'main\(\)'
    VAR = r'var'
    INT_TYPE = r'int'
    FLOAT_TYPE = r'float'
    CHAR_TYPE = r'char'
    FUNC = r'func'
    RETURN = r'return'
    VOID = r'void'
    INPUT = r'input'
    PRINT = r'print'
    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    FOR = r'for'
    TO = r'to'

    AND = r'&&'
    OR = r'\|\|'
    EQUAL = r'=='
    ASSIGN = r'='
    NOTEQUAL = r'!='
    LTEQUAL = r'<='
    GTEQUAL = r'>='
    LT = r'<'
    GT = r'>'

    # Check This (literals...)
    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    LPAR = r'\('
    RPAR = r'\)'
    LBRACKET = r'{'
    RBRACKET = r'}'
    COLON = r':'
    SEMICOLON = r';'
    COMMA = r'\,'



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

            