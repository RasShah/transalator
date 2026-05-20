import sys
from lexer import lexer
from parser import Parser


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        print("Enter your program:")
        code = sys.stdin.read()

    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        parser.parse_program()

        print("\nProgram is correct.")

        print("\nSymbol table:")
        for var, info in parser.symbol_table.items():
            print(f"{var}: type={info['type']}, value={info['value']}")

    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()