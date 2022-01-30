from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from tokens import Token
from typing import TypeVar, Generic

T = TypeVar('T')

class Visitor(ABC, Generic[T]):
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary) -> T:
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping) -> T:
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal) -> T:
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary) -> T:
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
        return visitor.visitBinaryExpr(self)

@dataclass
class Grouping(Expr):
    expression: Expr
    
    def accept(self, visitor:Visitor):
        return visitor.visitGroupingExpr(self)


@dataclass
class Literal(Expr):
    value: object
    
    def accept(self, visitor:Visitor):
        return visitor.visitLiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
        
    def accept(self, visitor:Visitor):
        return visitor.visitUnaryExpr(self)
