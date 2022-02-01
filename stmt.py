from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from expr import Expr
from tokens import Token

T = TypeVar('T')


class Visitor(ABC, Generic[T]) :
    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression ):
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: Print ):
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: Var ):
        pass


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


@dataclass
class Expression(Stmt):
    expression: Expr
    def accept(self, visitor: Visitor):
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expression: Expr
    def accept(self, visitor: Visitor):
        return visitor.visit_print_stmt(self)


@dataclass
class Var(Stmt):
    name: Token | None
    initializer: Expr | None
    def accept(self, visitor: Visitor):
        return visitor.visit_var_stmt(self)
        
