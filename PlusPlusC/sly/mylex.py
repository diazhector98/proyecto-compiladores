from sly import Lexer


class MyLexer(Lexer):
    # This is the set of tokens we are exporting to the Parser
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, OR, AND, EQUALITY, INEQUALITY, BIGGER, SMALLER, LEFT_PAR, RIGHT_PAR,
              STRING, IDENTIFIER}
    # Any literals we want to ignore
    ignore = ' \t'
    # Any literals we did not define as tokens, will be available for usage in the Parser
    literals = {'.', '!'}

    # The definition of each token in a regex pattern - Notice that the order MATTERS!! First match will be taken
    LEFT_PAR = r'\('
    RIGHT_PAR = r'\)'
    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*'
    DIVIDE = r'\/'
    OR = r'\|\|'
    AND = r'\&\&'
    EQUALITY = r'(===|==)'
    INEQUALITY = r'(!==|!=)'
    BIGGER = r'(>=|>)'
    SMALLER = r'(<=|<)'

    # This decorator allows us to add a logic before returning the matched token.
    @_(r"(0|[1-9][0-9]*)")
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    # Notice Identifier comes after string because most words in a string would be matched with the identifier pattern
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text