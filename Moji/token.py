# moji/token.py

################################################################################
# 1. CLASSE TOKEN
# Representa um único token encontrado pelo Lexer.
################################################################################

class Token:
    """
    Um objeto simples para armazenar o tipo do token e seu valor (opcional).

    Atributos:
        type (str): O tipo do token (ex: TT_OP_PLUS, TT_LIT_INT).
        value (any): O valor do token (ex: 123, "olá", ou o próprio emoji '➕').
    """

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        """
        Uma representação amigável para debug, ex: Token(TT_LIT_INT:123)
        """
        if self.value is not None:
            return f'Token({self.type}:{self.value})'
        return f'Token({self.type})'


################################################################################
# 2. CONSTANTES DE TIPOS DE TOKEN (TT = Token Type)
################################################################################

# --- Tokens que não são emojis (Literais, Identificadores) ---

# Um nome de variável (ex: 'idade')
TT_IDENTIFIER = 'IDENTIFIER'

# Literais (valores brutos)
TT_LIT_INT = 'LIT_INT'  # Ex: 10, 25
TT_LIT_REAL = 'LIT_REAL'  # Ex: 3.14
TT_LIT_STRING = 'LIT_STRING'  # Ex: "Olá, mundo!"

# Fim do arquivo
TT_EOF = 'EOF'  # End Of File

# --- Estrutura do Programa ---
TT_PROGRAM_START = 'PROGRAM_START'  # 🌱
TT_PROGRAM_END = 'PROGRAM_END'  # 🌳

# --- Blocos de Código ---
TT_BLOCK_START = 'BLOCK_START'  # 📦
TT_BLOCK_END = 'BLOCK_END'  # 📦⛔

# --- Declaração de Variáveis (Palavras-chave) ---
TT_KEYWORD_INT = 'KEYWORD_INT'  # 🔢
TT_KEYWORD_REAL = 'KEYWORD_REAL'  # 👽
TT_KEYWORD_STRING = 'KEYWORD_STRING'  # 💬

# --- Input / Output (Palavras-chave) ---
TT_KEYWORD_READ = 'KEYWORD_READ'  # 👀
TT_KEYWORD_PRINT = 'KEYWORD_PRINT'  # 🖨️

# --- Operações Matemáticas ---
TT_OP_PLUS = 'OP_PLUS'  # ➕
TT_OP_MINUS = 'OP_MINUS'  # ➖
TT_OP_MUL = 'OP_MUL'  # ✖️
TT_OP_DIV = 'OP_DIV'  # ➗

# --- Atribuição ---
TT_ASSIGN = 'ASSIGN'  # 👉

# --- Sintaxe ---
TT_COMMENT = 'COMMENT'  # 💭 (O Lexer pode ignorar isso)
TT_END_STATEMENT = 'END_STATEMENT'  # 🔚

# --- Condicionais (Palavras-chave) ---
TT_KEYWORD_IF = 'KEYWORD_IF'  # 🤔
TT_KEYWORD_ELIF = 'KEYWORD_ELIF'  # 🔀
TT_KEYWORD_ELSE = 'KEYWORD_ELSE'  # 🤨

# --- Funções (Palavras-chave) ---
TT_KEYWORD_FUN = 'KEYWORD_FUN'  # 🧩
TT_KEYWORD_RETURN = 'KEYWORD_RETURN'  # 🔙

# --- Lógica & Comparação ---
TT_COMP_EQ = 'COMP_EQ'  # ⚖️ (Igual a)
TT_COMP_GT = 'COMP_GT'  # ⬆️ (Maior que)
TT_COMP_LT = 'COMP_LT'  # ⬇️ (Menor que)
TT_LOGIC_NOT = 'LOGIC_NOT'  # 🚫 (Negação)

# --- Listas (Palavras-chave) ---
TT_KEYWORD_LIST = 'KEYWORD_LIST'  # 📜
TT_KEYWORD_APPEND = 'KEYWORD_APPEND'  # ➕📜
TT_KEYWORD_REMOVE = 'KEYWORD_REMOVE'  # ➖📜

# --- Sistema (Palavras-chave) ---
TT_KEYWORD_IMPORT = 'KEYWORD_IMPORT'  # ⚙️
TT_KEYWORD_SAVE = 'KEYWORD_SAVE'  # 💾
TT_KEYWORD_SLEEP = 'KEYWORD_SLEEP'  # ⏱️

################################################################################
# 3. MAPEAMENTO DE EMOJIS (Para ajudar o Lexer)
# Mapeia o caractere emoji para seu TIPO de token correspondente.
################################################################################

# Este dicionário será usado pelo Lexer para identificar rapidamente
# os tokens de um único caractere (ou emoji).
EMOJI_KEYWORDS = {
    # Estrutura
    '🌱': TT_PROGRAM_START,
    '🌳': TT_PROGRAM_END,

    # Blocos
    '📦': TT_BLOCK_START,
    '📦⛔': TT_BLOCK_END,  # Nota: Este tem 2 caracteres, o Lexer precisará tratar isso

    # Variáveis
    '🔢': TT_KEYWORD_INT,
    '👽': TT_KEYWORD_REAL,
    '💬': TT_KEYWORD_STRING,

    # I/O
    '👀': TT_KEYWORD_READ,
    '🖨️': TT_KEYWORD_PRINT,

    # Matemática
    '➕': TT_OP_PLUS,
    '➖': TT_OP_MINUS,
    '✖️': TT_OP_MUL,
    '➗': TT_OP_DIV,

    # Atribuição
    '👉': TT_ASSIGN,

    # Sintaxe
    '💭': TT_COMMENT,
    '🔚': TT_END_STATEMENT,

    # Condicionais
    '🤔': TT_KEYWORD_IF,
    '🔀': TT_KEYWORD_ELIF,
    '🤨': TT_KEYWORD_ELSE,

    # Funções
    '🧩': TT_KEYWORD_FUN,
    '🔙': TT_KEYWORD_RETURN,

    # Lógica
    '⚖️': TT_COMP_EQ,
    '⬆️': TT_COMP_GT,
    '⬇️': TT_COMP_LT,
    '🚫': TT_LOGIC_NOT,

    # Listas
    '📜': TT_KEYWORD_LIST,
    '➕📜': TT_KEYWORD_APPEND,  # Nota: 2 caracteres
    '➖📜': TT_KEYWORD_REMOVE,  # Nota: 2 caracteres

    # Sistema
    '⚙️': TT_KEYWORD_IMPORT,
    '💾': TT_KEYWORD_SAVE,
    '⏱️': TT_KEYWORD_SLEEP,
}