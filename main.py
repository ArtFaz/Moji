# main.py

import sys
import os
from Moji.lexer import Lexer
from Moji.parser import Parser, SyntaxError
from Moji.interpreter import Interpreter, RuntimeError


def main():
    # 1. Check if a file was provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.moji>")
        sys.exit(1)

    filepath = sys.argv[1]

    # 2. Check if the file exists
    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'")
        sys.exit(1)

    # 3. Read the code from the file (with UTF-8 encoding for emojis)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit(1)

    if not code:
        print("File is empty.")
        return

    # 4. Run the pipeline (Lexer -> Parser -> Interpreter)
    try:
        # Lexer
        lexer = Lexer(code)
        tokens = lexer.make_tokens()

        # Parser
        parser = Parser(tokens)
        ast = parser.parse()

        # Interpreter
        interpreter = Interpreter()
        interpreter.run(ast)

    except SyntaxError as e:
        # Error caught by the Parser
        print(f"!!! Syntax Error !!!")
        print(e)

    except RuntimeError as e:
        # Error caught by the Interpreter
        print(f"!!! Runtime Error !!!")
        print(e)

    except Exception as e:
        # Other unexpected error (likely a bug in the interpreter itself)
        print(f"!!! Unexpected Error (Python) !!!")
        print(e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()