import sys
from enum import Enum
import typing

class TokenType(Enum):
    LEFT_PAREN    = 0
    RIGHT_PAREN   = 1
    LEFT_BRACE    = 2
    RIGHT_BRACE   = 3
    COMMA         = 4
    DOT           = 5
    MINUS         = 6
    PLUS          = 7
    SEMICOLON     = 8
    SLASH         = 9
    STAR          = 10
    BANG          = 11
    BANG_EQUAL    = 12
    EQUAL         = 13
    EQUAL_EQUAL   = 14
    GREATER       = 15
    GREATER_EQUAL = 16
    LESS          = 17
    LESS_EQUAL    = 18
    IDENTIFIER    = 19
    STRING        = 20
    NUMBER        = 20
    AND           = 21
    CLASS         = 21
    ELSE          = 22
    FALSE         = 23
    FUN           = 24
    FOR           = 25
    IF            = 26
    NIL           = 27
    OR            = 28
    PRINT         = 29
    RETURN        = 30
    SUPER         = 31
    THIS          = 32
    TRUE          = 33
    VAR           = 34
    WHILE         = 35
    EOF           = 36

keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}
    

    
class Token:
    type: TokenType
    lexeme: str
    literal: typing.Any
    line: int 

    def __init__(self, type: TokenType, lexeme: str, literal: object | None, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self):
        return f'{self.type} {self.lexeme} {self.literal}'


class Scanner:
    source: str
    tokens: list[Token]
    start: int
    current: int
    line: int

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        
    def scan_tokens(self):
        while (not self.is_at_end()):
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if   c == '(': self.add_token(TokenType.LEFT_PAREN)
        elif c == ')': self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{': self.add_token(TokenType.LEFT_BRACE)
        elif c == '}': self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',': self.add_token(TokenType.COMMA)
        elif c == '.': self.add_token(TokenType.DOT)
        elif c == '-': self.add_token(TokenType.MINUS)
        elif c == '+': self.add_token(TokenType.PLUS)
        elif c == ';': self.add_token(TokenType.SEMICOLON)
        elif c == '*': self.add_token(TokenType.STAR)
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL if self.match('=') else TokenType.EQUAL_EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if (self.match('/')):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '"':
            self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()
        elif c in [' ', '\r', '\t']:
            pass
        elif '\n':
            self.line += 1
        else: Lox.error(self.line, 'Unexpected character.')
            
        
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    
    def add_token(self, type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
        
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1

        self.advance()

        if self.is_at_end():
            Lox.error(self.line, 'Unterminated string.')
            return
        
        self.advance()

        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_digit(_self, c: str) -> bool:
        return c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def is_alpha(_self, c: str) -> bool:
        return ('a' <= c <= 'z') or ('A' <= c <='Z')

    def is_alpha_number(self, c: str):
        return self.is_digit(c) or self.is_alpha(c)
    
    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, self.source[self.start:self.current])

    def identifier(self):
        while self.is_alpha_number(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        type = keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)

        
class Lox:
    has_error = False

    @classmethod
    def main(cls):
        print(sys.argv)
        if len(sys.argv) == 1:
            cls.run_prompt()
        elif len(sys.argv) == 2:
            cls.run_file(sys.argv[0])
        else:
            print('Usage: jlox [script]')
            sys.exit(0)

    @classmethod
    def run_file(cls, path: str):
        source = open(path, 'r').read()
        cls.run(source)

    @classmethod
    def run_prompt(cls):
        while True:
            print('> ')
            line = input()
            if len(line) == 0:
                return
            cls.run(line)
            hadError = False

    @classmethod
    def run(cls, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f'[line {line}] Error {where} : {message}', file=sys.stderr)
        cls.has_error = True



if __name__ == '__main__':
    lox = Lox()
    lox.main()
