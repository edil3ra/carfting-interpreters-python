from abc import ABC
from typing import List

from interpreter import Interpreter


class LoxCallable(ABC):
    def call(self, interpreter: Interpreter, argumens: List[object]):
        return time.time()

    def artiry(self) -> int:
        return 0

    def __str__(self) -> str:
        return ''
