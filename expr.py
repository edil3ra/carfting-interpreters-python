from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from tokens import Token
from typing import TypeVar, Generic

T = TypeVar('T')

class Visitor(ABC, Generic[T]):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> T:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping) -> T:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal) -> T:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> T:
        pass
        

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor:Visitor):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr
        
    def accept(self, visitor:Visitor):
        return visitor.visit_binary_expr(self)

@dataclass
class Grouping(Expr):
    expression: Expr
    
    def accept(self, visitor:Visitor):
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: object
    
    def accept(self, visitor:Visitor):
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
        
    def accept(self, visitor:Visitor):
        return visitor.visit_unary_expr(self)
