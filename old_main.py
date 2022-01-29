import sys


def main():
    print(sys.argv)
    if len(sys.argv) == 1:
        run_prompt()
    elif len(sys.argv) == 2:
        run_file(sys.argv[0])
    else:
        print('Usage: jlox [script]')
        sys.exit(0)



def run_file(path: str):
    source = open(path, 'r').read()
    run(source)


def run_prompt():
    while True:
        print('> ')
        line = input()
        if len(line) == 0:
            return
        run(line)
        

def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    for token in tokens:
        print(token)


def error(line: int, message: str):
    report(line, "", message)


    
def report(line: int, where: str, message: str):
    print(f'[line {line}] Error {where} : {message}', file=sys.stderr)
    

        
if __name__ == '__main__':
    main()
