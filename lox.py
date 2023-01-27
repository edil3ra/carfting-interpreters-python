import sys
from tokens import Token
from token_type import TokenType
from ast_printer import AstPrinter
from runtimeerror import RuntimeError

class Lox:
    has_error = False
    has_runtime_error = False

    @classmethod
    def main(cls):
        cls.interpreter = Interpreter()
        
        if len(sys.argv) == 1:
            cls.run_prompt()
        elif len(sys.argv) == 2:
            cls.run_file(sys.argv[1])
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
            cls.has_error = False

    @classmethod
    def run(cls, source: str):
        scanner = Scanner(source.strip())
        tokens = scanner.scan_tokens()
        statements = Parser(tokens).parse()
        cls.interpreter.interpret(statements)

        if (cls.has_error):
            sys.exit(65)

    @classmethod
    def runtime_error(cls, error: RuntimeError):
        print(f'{error.message}\n[line {error.token.line}]')
        cls.has_runtime_error = True

    @classmethod
    def error_line(cls, line: int, message: str):
        cls.report(line, "", message)
        
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


from scanner import Scanner
from parsers import Parser
from interpreter import Interpreter
