import typing
from token_type import TokenType
from dataclasses import dataclass

@dataclass
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

