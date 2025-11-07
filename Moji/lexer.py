# moji/lexer.py

# Importa as definições de Token e o mapa de Emojis do arquivo token.py
from .token import (
    Token, EMOJI_KEYWORDS,
    TT_LIT_INT, TT_LIT_REAL, TT_LIT_STRING,
    TT_IDENTIFIER, TT_EOF
)


################################################################################
# 1. CLASSE LEXER
# Responsável por pegar o texto-fonte e quebrá-lo em uma lista de Tokens.
################################################################################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0  # Posição atual no texto
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def error(self, message):
        """ Lança uma exceção em caso de erro léxico. """
        # Você pode tornar isso mais robusto no futuro (ex: com números de linha/coluna)
        raise Exception(f"Erro Léxico: {message}")

    def advance(self):
        """ Move o ponteiro `pos` para o próximo caractere no texto. """
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None  # Indica Fim do Arquivo (EOF)

    def peek(self, n=1):
        """
        Olha 'n' caracteres à frente (lookahead) sem consumir o caractere.
        Retorna None se estiver fora dos limites.
        """
        peek_pos = self.pos + n
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        """ Pula caracteres de espaço em branco (espaço, tab, newline). """
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        """ Pula uma linha inteira de comentário (tudo após '💭'). """
        # Avança além do emoji '💭'
        self.advance()
        # Continua avançando até encontrar uma nova linha ou o fim do arquivo
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def make_number(self):
        """ Processa um número (inteiro ou real). """
        num_str = ''
        dot_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break  # Segundo ponto decimal, para o loop
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_LIT_INT, int(num_str))
        else:
            return Token(TT_LIT_REAL, float(num_str))

    def make_string(self):
        """ Processa uma string literal (entre aspas). """
        str_val = ''
        self.advance()  # Pula o '"' inicial

        while self.current_char is not None and self.current_char != '"':
            str_val += self.current_char
            self.advance()

        if self.current_char is None:
            self.error("String não fechada.")

        self.advance()  # Pula o '"' final
        return Token(TT_LIT_STRING, str_val)

    def make_identifier(self):
        """ Processa um identificador (nome de variável/função). """
        ident_str = ''
        # Nomes podem conter letras, números (mas não no início) e underscore
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            ident_str += self.current_char
            self.advance()

        # Nota: Por enquanto, não estamos verificando se palavras-chave (como 'if')
        # são usadas como identificadores, pois nossas palavras-chave são emojis.
        return Token(TT_IDENTIFIER, ident_str)

    def make_tokens(self):
        """
        O método principal. Gera uma lista de todos os tokens do texto-fonte.
        """
        tokens = []

        while self.current_char is not None:

            # 1. Pular Espaços em Branco
            if self.current_char in ' \t\n\r':
                self.advance()
                continue

            # 2. Pular Comentários
            if self.current_char == '💭':
                self.skip_comment()
                continue

            # 3. Números (Inteiros e Reais)
            if self.current_char.isdigit():
                tokens.append(self.make_number())
                continue

            # 4. Strings
            if self.current_char == '"':
                tokens.append(self.make_string())
                continue

            # 5. Identificadores (Nomes de variáveis)
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.make_identifier())
                continue

            # 6. Emojis (com Lookahead)

            # --- Lógica de Lookahead ---
            # Primeiro, tentamos ver se é um token de 2 caracteres
            peeked_char = self.peek()
            if peeked_char is not None:
                two_char_emoji = self.current_char + peeked_char
                if two_char_emoji in EMOJI_KEYWORDS:
                    token_type = EMOJI_KEYWORDS[two_char_emoji]
                    tokens.append(Token(token_type, two_char_emoji))
                    self.advance()  # Avança o 1º caractere
                    self.advance()  # Avança o 2º caractere
                    continue

            # Se não for um token de 2 caracteres, tentamos um de 1 caractere
            if self.current_char in EMOJI_KEYWORDS:
                token_type = EMOJI_KEYWORDS[self.current_char]
                emoji_val = self.current_char
                tokens.append(Token(token_type, emoji_val))
                self.advance()
                continue

            # 7. Erro
            # Se chegou até aqui, não reconhecemos o caractere
            self.error(f"Caractere ilegal ou emoji desconhecido: '{self.current_char}'")

        # Fim do loop, adiciona o token de Fim de Arquivo
        tokens.append(Token(TT_EOF))
        return tokens


################################################################################
# 3. Bloco de Teste
# (Para executar este arquivo diretamente: python -m moji.lexer)
################################################################################

if __name__ == '__main__':
    # Código de exemplo do seu "hello_world.moji"
    test_code = """
    🌱 💭 Este é um programa de teste!

    💬 meuNome 👉 "Mojji" 🔚
    🖨️ "Olá, " ➕ meuNome 🔚

    🔢 x 👉 10 🔚
    🤔 x ⚖️ 10 📦
        🖨️ "x é 10!" 🔚
    📦⛔

    🌳
    """

    print(f"--- Testando Lexer com o código: ---\n{test_code}")

    try:
        lexer = Lexer(test_code)
        tokens = lexer.make_tokens()

        print("--- Tokens Gerados ---")
        for token in tokens:
            print(token)

    except Exception as e:
        print(f"\n!!! ERRO NO LEXER: {e}")