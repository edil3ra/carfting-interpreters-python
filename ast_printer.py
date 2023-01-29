from typing import cast
from typing import List

import expr
import stmt
from tokens import Token


class AstPrinter(expr.Visitor, stmt.Visitor):
    def print(self, expr_or_stmt: expr.Expr | stmt.Stmt) -> str:
        return cast(str, expr_or_stmt.accept(self))

    def print_statements(self, xs) -> List[str]:
        return [self.print(x) for x in xs]

    def visit_binary_expr(self, expr: expr.Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: expr.Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: expr.Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: expr.Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: expr.Variable) -> str:
        return expr.name.lexeme

    def visit_assign_expr(self, expr: expr.Assign) -> str:
        return "to implement"

    def visit_print_stmt(self, stmt: stmt.Print) -> str:
        return self._parenthesize("print", stmt.expression)

    def visit_expression_stmt(self, stmt: stmt.Expression) -> str:
        return self._parenthesize(";", stmt.expression)

    def visit_var_stmt(self, stmt: stmt.Var) -> str:
        if stmt.initializer is None:
            return self._parenthesize2("var", stmt.name)
        return self._parenthesize2("var", stmt.name, "=", stmt.initializer)

    def _parenthesize(self, name: str, *exprs: expr.Expr) -> str:
        s = "("
        s += name
        for expr in exprs:
            s += " "
            s += expr.accept(self)
        s += ")"
        return s

    def _parenthesize2(self, name: str, *parts):
        s = "("
        s += name
        self.transform(*parts)
        s += ")"
        return s

    def transform(self, s: str, *parts):
        for part in parts:
            s += ". "
            if part is expr.Expr:
                s += part.accept(self)
            elif part is stmt.Stmt:
                s += part.accept(self)
            elif part is Token:
                s += part.accept(self)
            elif part is list:
                self.transform(s, *part)
            else:
                s += part
