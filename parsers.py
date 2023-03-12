from typing import cast
from typing import List

from expr import *
from lox import Lox
from stmt import *
from token_type import TokenType
from tokens import Token


class ParseError(Exception):
    pass


class Parser:
    tokens: List[Token]
    current: int

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def declaration(self) -> Stmt | Expr | None:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except (ParseError):
            self.synchronize()
            return None

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Except variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, 'Except ";" after variable declaration.')
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):
            statements = self.block()
            return Block(statements)
        return self.expression_statement()

    def for_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Except '(' at the beggining of for.")

        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Except ';' after loop condition.")

        increment = None
        if not self.check(TokenType.SEMICOLON):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Except ')' after loop condition.")

        body = self.statement()

        if increment is not None:
            body = Block([body, increment])

        if condition is None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])
        return body

    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Excepct '( after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Excepct ') after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return If(condition, then_branch, else_branch)

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Except ')' after condition.")
        body = self.statement()
        return While(condition, body)

    def block(self) -> List[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, 'Except "}" after block.')
        return statements

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, 'Except ";" after value.')
        return Print(value)

    def expression_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, 'Except ";" after value.')
        return Expression(value)

    def expression(self):
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self._or()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if type(expr) is Variable:
                name = cast(Variable, expr).name
                return Assign(name, value)
            self.error(equals, "invalid assignment target.")
        return expr

    def _or(self) -> Expr:
        expr = self._and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self._and()
            expr = Logical(expr, operator, right)
        return expr

    def _and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        return expr

    def finish_call(self, calee: Expr) -> Expr:
        arguments: List[Expr] = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, "Except ')' after arguments.")
        return Call(calee, paren, arguments)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Except ')' after expression.")
            return Grouping(expr)
        raise self.error(self.peek(), "Except expression.")

    def match(self, *tokens) -> bool:
        for token_type in tokens:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def consume(self, token: TokenType, message: str):
        if self.check(token):
            return self.advance()
        return self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        Lox.error(token, message)
        raise ParseError()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return
            self.advance()
