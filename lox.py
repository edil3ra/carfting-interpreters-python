import sys

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
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f'[line {line}] Error {where} : {message}', file=sys.stderr)
        cls.has_error = True
