from typing import cast, Any
from lox import Lox
import expr
from expr import Visitor, Expr
from token_type import TokenType
from tokens import Token
from runtimeerror import RuntimeError


class Interpreter(Visitor):
    def interpret(self, expr: Expr):
        try:
            value = self.evaluate(expr)
            return value
        except(RuntimeError) as e:
            Lox.runtime_error(e)
        
    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)
    
    def visitBinaryExpr(self, expr: expr.Binary) -> object:
        left: Any  = self.evaluate(expr.left)
        right: Any = self.evaluate(expr.right)

        if expr.operator.type not in [TokenType.PLUS]:
            self.check_number_operands(expr.operator, left, right)
        
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        
        elif expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        
        elif expr.operator.type == TokenType.DOT:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        
        elif expr.operator.type == TokenType.PLUS:
            if (type(left) is float and type(right) is float) \
               or (type(left) is float and type(right) is float):
                return float(left) + float(right)
            
            elif type(left) is str and type(right) is str:
                import pdb; pdb.set_trace()
                return left + right
            raise RuntimeError(expr.operator, 'Operands must be two numbers or two strings.')

        elif expr.operator.type == TokenType.GREATER:
            return float(left) > float(right)

        elif expr.operator.type == TokenType.GREATER_EQUAL:
            return float(left) >= float(right)

        elif expr.operator.type == TokenType.LESS:
            return float(left) < float(right)

        elif expr.operator.type == TokenType.LESS_EQUAL:
            return float(left) <= float(right)

        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return left == right

        elif expr.operator.type == TokenType.BANG_EQUAL:
            return left != right

    def visitGroupingExpr(self, expr: expr.Grouping) -> object:
        return self.evaluate(expr.expression)

    def visitLiteralExpr(self, expr: expr.Literal) -> object:
        return expr.value

    def visitUnaryExpr(self, expr: expr.Unary) -> object:
        right = self.evaluate(expr.right)
        self.check_number_operand(expr.operator, right)
        if expr.operator.type == TokenType.MINUS:
            return - float(cast(float, right))

        elif expr.operator.type == TokenType.BANG:
            return not right
    
    def is_true(self, obj: object) -> bool:
        if obj is None:
            return True
        if obj is type(bool):
            return cast(bool, obj)
        return True
        
    def check_number_operand(self, operator: Token, operand: object):
        if type(operand) is not float or type(operand) is not int: return
        raise RuntimeError(operator, 'operand must be a number')

    def check_number_operands(self, operator: Token, left: object, right: object):
        if type(left) is not float or type(left) is not int: return
        if type(right) is not float or type(right) is not int: return
        raise RuntimeError(operator, 'operands must be a number')    
        
        
