from typing import Any
from typing import cast
from typing import List

import expr
import stmt
from environment import Environment
from lox import Lox
from runtimeerror import RuntimeError
from token_type import TokenType
from tokens import Token


class Interpreter(stmt.Visitor, expr.Visitor):
    environment: Environment

    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements: List[stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except (RuntimeError) as e:
            Lox.runtime_error(e)

    def execute(self, stmt: stmt.Stmt):
        stmt.accept(self)

    def execute_block(self, statements: List[stmt.Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def evaluate(self, expr: expr.Expr) -> object:
        return expr.accept(self)

    def visit_expression_stmt(self, stmt: stmt.Expression) -> None:
        self.evaluate(stmt.expression)
        return None

    def visit_block_stmt(self, stmt: stmt.Block):
        self.execute_block(stmt.statements, Environment())

    def visit_if_stmt(self, stmt: stmt.If) -> None:
        if self.is_true(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        else:
            self.execute(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt: stmt.Print) -> None:
        value = self.evaluate(stmt.expression)
        print(value)
        return None

    def visit_var_stmt(self, stmt: stmt.Var) -> None:
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_binary_expr(self, expr: expr.Binary) -> object:
        left: Any = self.evaluate(expr.left)
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
            if (type(left) is float and type(right) is float) or (
                type(left) is float and type(right) is float
            ):
                return float(left) + float(right)

            elif type(left) is str and type(right) is str:
                return left + right
            raise RuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )

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

    def visit_grouping_expr(self, expr: expr.Grouping) -> object:
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: expr.Literal) -> object:
        return expr.value

    def visit_variable_expr(self, expr: expr.Variable) -> object:
        return self.environment.get(expr.name)

    def visit_unary_expr(self, expr: expr.Unary) -> object:
        right = self.evaluate(expr.right)
        self.check_number_operand(expr.operator, right)
        if expr.operator.type == TokenType.MINUS:
            return -float(cast(float, right))

        elif expr.operator.type == TokenType.BANG:
            return not right

    def visit_assign_expr(self, expr: expr.Assign) -> object:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def is_true(self, obj: object) -> bool:
        if obj is None:
            return True
        if obj is type(bool):
            return cast(bool, obj)
        return True

    def check_number_operand(self, operator: Token, operand: object):
        if type(operand) is not float or type(operand) is not int:
            return
        raise RuntimeError(operator, "operand must be a number")

    def check_number_operands(self, operator: Token, left: object, right: object):
        if type(left) is not float or type(left) is not int:
            return
        if type(right) is not float or type(right) is not int:
            return
        raise RuntimeError(operator, "operands must be a number")
