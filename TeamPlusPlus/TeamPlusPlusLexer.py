from sly import Lexer

class TeamPlusPlusLexer(Lexer):
    
    #Lenguage tokens
    tokens = {

        ID,
        PROGRAM,
        MAIN,

        #For variables
        VAR,
        INT,
        FLOAT,
        CHAR,
        STRING,

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
    STRING = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PROGRAM = r'program'
    MAIN = r'main\(\)'
    VAR = r'var'
    INT = r'int'
    FLOAT = r'float'
    CHAR = r'char'
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


    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
      t.value = t.value
      return t
    
    @_(r'\n+')
    def count_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Lexical error. Illegal character '%s'" % (self.lineno, t.value[0]))
        self.index += 1

Tokens = TeamPlusPlusLexer.tokens

            