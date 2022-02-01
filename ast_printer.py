from typing import List, cast

import expr
import stmt


class AstPrinter(expr.Visitor, stmt.Visitor):
    def print(self, expr_or_stmt: expr.Expr | stmt.Stmt ) -> str:
        return cast(str, expr_or_stmt.accept(self))

    def print_statements(self, xs ) -> List[str]:
        return [self.print(x) for x in xs]
    
    def visit_binary_expr(self, expr: expr.Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: expr.Grouping) -> str:
        return self._parenthesize('group', expr.expression)

    def visit_literal_expr(self, expr: expr.Literal) -> str:
        if (expr.value is None):
            return 'nil'
        return str(expr.value)

    def visit_unary_expr(self, expr: expr.Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_print_stmt(self, stmt: stmt.Print) -> str:
        return self._parenthesize("print", stmt.expression)

    def visit_expression_stmt(self, stmt: stmt.Expression) -> str:
        return self._parenthesize(";", stmt.expression)
    
    def _parenthesize(self, name: str, *exprs: expr.Expr) -> str:
        s = '('
        s += name
        for expr in exprs:
            s += ' '
            s += expr.accept(self)
        s += ')'
        return s
