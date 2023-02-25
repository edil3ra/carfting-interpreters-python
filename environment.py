from typing import Dict, Any
from tokens import Token
from runtimeerror import RuntimeError

class Environment:
    values: Dict
    enclosing: "Environment"

    def __init__(self, enclosing = None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name: str, value: Any):
        self.values[name] = value
    
    def get(self, name: Token) -> Any:
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeError(name, f'Undefined variable "{name.lexeme}".')

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(name, f'Undefined variable "{name.lexeme}".')
