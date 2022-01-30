from lox import Lox
import expr
from tokens import Token
from token_type import TokenType
from ast_printer import AstPrinter

def test_expr():
    expression = expr.Binary(
        expr.Unary(
            Token(TokenType.MINUS, '-', None, 1),
            expr.Literal(123),
        ),
        Token(TokenType.STAR, '*', None, 1),
        expr.Grouping(
            expr.Literal(45.67)
        )
    )
    return expression.accept(AstPrinter())

if __name__ == '__main__':
    lox = Lox()
    lox.main()
    
