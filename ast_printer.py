import expr
from expr import Visitor, Expr

class AstPrinter(Visitor):
    def visitBinaryExpr(self, expr: expr.Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: expr.Grouping) -> str:
        return self._parenthesize('group', expr.expression)

    def visitLiteralExpr(self, expr: expr.Literal) -> str:
        if (expr.value is None):
            return 'nil'
        return str(expr.value)

    def visitUnaryExpr(self, expr: expr.Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        s = '('
        s += name
        for expr in exprs:
            s += ' '
            s += expr.accept(self)
        s += ')'
        return s
