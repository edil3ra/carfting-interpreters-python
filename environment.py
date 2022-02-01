from typing import Dict, Any
from tokens import Token
from runtimeerror import RuntimeError

class Environment:
    values: Dict
    def __init__(self):
        self.values = {}

    def define(self, name: str, value: Any):
        self.values[name] = value
    
    def get(self, name: Token):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        raise RuntimeError(name, f'Undefined variable "{name.lexeme}".')
