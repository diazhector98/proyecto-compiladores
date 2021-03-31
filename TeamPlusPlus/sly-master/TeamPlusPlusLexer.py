from sly import Lexer

class TeamPlusPlusLexer(Lexer):
    
    #Lenguage tokens
    tokens = {

        ID,
        PROGRAM,
        PRINCIPAL,

        #For variables
        VAR,
        INT,
        FLOAT,
        CHAR,

        #For functions
        FUNC,
        RETURN,
        VOID,

        #For Actions
        READ,
        WRITE,

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
    PROGRAM = r'programa'
    PRINCIPAL = r'principal\(\)'
    VAR = r'var'
    INT = r'int'
    FLOAT = r'float'
    CHAR = r'char'
    FUNC = r'func'
    RETURN = r'return'
    VOID = r'void'
    READ = r'read'
    WRITE = r'write'
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

            