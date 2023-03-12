import time
from abc import ABC
from typing import List
from interpreter import Interpreter
from loxCallable import LoxCallable


class getTime(LoxCallable):
    def call(self, interpreter: Interpreter, argumens: List[object]):
        return time.time()

    def artiry(self) -> int:
        return 0

    def __str__(self) -> str:
        return '<native fn>'
