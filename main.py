# main.py

import sys
import os
from Moji.lexer import Lexer
from Moji.parser import Parser, SyntaxError
from Moji.interpreter import Interpreter, RuntimeError


def main():
    # 1. Verificar se um arquivo foi fornecido
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo.moji>")
        sys.exit(1)

    filepath = sys.argv[1]

    # 2. Verificar se o arquivo existe
    if not os.path.exists(filepath):
        print(f"Erro: Arquivo não encontrado em '{filepath}'")
        sys.exit(1)

    # 3. Ler o código do arquivo (com encoding UTF-8 para os emojis)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    if not code:
        print("Arquivo está vazio.")
        return

    # 4. Executar a esteira (Lexer -> Parser -> Interpreter)
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
        # Erro pego pelo Parser
        print(f"!!! Erro de Sintaxe !!!")
        print(e)

    except RuntimeError as e:
        # Erro pego pelo Interpreter
        print(f"!!! Erro de Execução !!!")
        print(e)

    except Exception as e:
        # Outro erro inesperado (provavelmente um bug no interpretador)
        print(f"!!! Erro Inesperado (Python) !!!")
        print(e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()