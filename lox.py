import sys
from tokens import Token
from token_type import TokenType
from ast_printer import AstPrinter


class Lox:
    has_error = False

    @classmethod
    def main(cls):
        if len(sys.argv) == 1:
            cls.run_prompt()
        elif len(sys.argv) == 2:
            cls.run_file(sys.argv[0])
        else:
            print('Usage: jlox [script]')
            sys.exit(0)

    @classmethod
    def run_file(cls, path: str):
        source = open(path, 'r').read()
        cls.run(source)

    @classmethod
    def run_prompt(cls):
        while True:
            print('> ', end='')
            line = input()
            if len(line) == 0:
                return
            cls.run(line)
            hadError = False

    @classmethod
    def run(cls, source: str):
        from scanner import Scanner
        from parsers import Parser
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        expression = Parser(tokens).parse()
        print(AstPrinter().print(expression))


    @classmethod
    def error(cls, token: Token, message: str):
        if token.type == TokenType.EOF:
            cls.report(token.line, "at end", message)
        else:
            cls.report(token.line, f"at '{token.lexeme}'", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f'[line {line}] Error {where} : {message}', file=sys.stderr)
        cls.has_error = True
