from abc import ABC
from typing import List
import stmt
from interpreter import Interpreter
from environment import Environment

class LoxCallable(ABC):
    def call(self, interpreter: Interpreter, arguments: List[object]):
        pass

    def artiry(self) -> int:
        return 0

    def __str__(self) -> str:
        return ''


class LoxFunction(LoxCallable):
    def __init__(self, declaration: stmt.Function):
        self.declaration: stmt.Function = declaration

    def call(self, interpreter: Interpreter, arguments: List[object]):
        environment: Environment = Environment(interpreter.globals)
        for i in range len(self.declaration.parameters):
            environment.define(self.declaration.parameters[0].lexeme, arguments[0])
        interpreter.execute_block(self.declaration.body, environment)

    def __str__(self) -> str:
        return f'<fn {self.declaration.name.lexeme}>'
    
    
