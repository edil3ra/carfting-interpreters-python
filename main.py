import expr
from ast_printer import AstPrinter
from lox import Lox
from token_type import TokenType
from tokens import Token


def test_expr():
    expression = expr.Binary(
        expr.Unary(
            Token(TokenType.MINUS, "-", None, 1),
            expr.Literal(123),
        ),
        Token(TokenType.STAR, "*", None, 1),
        expr.Grouping(expr.Literal(45.67)),
    )
    return AstPrinter().print(expression)


if __name__ == "__main__":
    lox = Lox()
    lox.main()
