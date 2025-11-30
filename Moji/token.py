# moji/token.py

################################################################################
# 1. TOKEN CLASS
# Represents a single token found by the Lexer.
################################################################################

class Token:
    """
    A simple object to store the token type and its (optional) value.

    Attributes:
        type (str): The type of the token (e.g., TT_OP_PLUS, TT_LIT_INT).
        value (any): The value of the token (e.g., 123, "hello", or the emoji '➕' itself).
    """

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        """
        A friendly representation for debugging, e.g.: Token(TT_LIT_INT:123)
        """
        if self.value is not None:
            return f'Token({self.type}:{self.value})'
        return f'Token({self.type})'


################################################################################
# 2. TOKEN TYPE CONSTANTS (TT = Token Type)
################################################################################

# --- Non-Emoji Tokens (Literals, Identifiers) ---

# A variable name (e.g., 'age')
TT_IDENTIFIER = 'IDENTIFIER'

# Literals (raw values)
TT_LIT_INT = 'LIT_INT'      # e.g.: 10, 25
TT_LIT_REAL = 'LIT_REAL'    # e.g.: 3.14
TT_LIT_STRING = 'LIT_STRING'  # e.g.: "Hello, world!"

# End of file
TT_EOF = 'EOF'  # End Of File

# --- Program Structure ---
TT_PROGRAM_START = 'PROGRAM_START'  # 🌱
TT_PROGRAM_END = 'PROGRAM_END'      # 🌳

# --- Code Blocks ---
TT_BLOCK_START = 'BLOCK_START'  # 📦
TT_BLOCK_END = 'BLOCK_END'      # 📦⛔

# --- Variable Declaration (Keywords) ---
TT_KEYWORD_INT = 'KEYWORD_INT'      # 🔢
TT_KEYWORD_REAL = 'KEYWORD_REAL'    # 👽
TT_KEYWORD_STRING = 'KEYWORD_STRING'  # 💬

# --- Input / Output (Keywords) ---
TT_KEYWORD_READ = 'KEYWORD_READ'    # 👀
TT_KEYWORD_PRINT = 'KEYWORD_PRINT'  # 🖨️

# --- Mathematical Operations ---
TT_OP_PLUS = 'OP_PLUS'    # ➕
TT_OP_MINUS = 'OP_MINUS'  # ➖
TT_OP_MUL = 'OP_MUL'      # ✖️
TT_OP_DIV = 'OP_DIV'      # ➗

# --- Assignment ---
TT_ASSIGN = 'ASSIGN'  # 👉

# --- Syntax ---
TT_COMMENT = 'COMMENT'          # 💭
TT_END_STATEMENT = 'END_STATEMENT'  # 🔚

# --- Conditionals (Keywords) ---
TT_KEYWORD_IF = 'KEYWORD_IF'      # 🤔
TT_KEYWORD_ELIF = 'KEYWORD_ELIF'  # 🔀
TT_KEYWORD_ELSE = 'KEYWORD_ELSE'  # 🤨

# --- Functions (Keywords) ---
TT_KEYWORD_FUN = 'KEYWORD_FUN'        # 🧩
TT_KEYWORD_RETURN = 'KEYWORD_RETURN'  # 🔙
TT_KEYWORD_CALL = 'KEYWORD_CALL'      # 📞 (NOVO)

# --- Loops (Keywords) --- (NOVO)
TT_KEYWORD_WHILE = 'KEYWORD_WHILE'  # ⏳ (NOVO)
TT_KEYWORD_FOR = 'KEYWORD_FOR'      # 🚶 (NOVO)

# --- Logic & Comparison ---
TT_COMP_EQ = 'COMP_EQ'      # ⚖️ (Equal to)
TT_COMP_GT = 'COMP_GT'      # ⬆️ (Greater than)
TT_COMP_LT = 'COMP_LT'      # ⬇️ (Less than)
TT_LOGIC_NOT = 'LOGIC_NOT'  # 🚫 (Negation)
TT_LOGIC_AND = 'LOGIC_AND'    # 🤝 (NOVO)
TT_LOGIC_OR = 'LOGIC_OR'      # 🌀 (NOVO)

# --- Lists (Keywords) ---
TT_KEYWORD_LIST = 'KEYWORD_LIST'      # 📜
TT_KEYWORD_APPEND = 'KEYWORD_APPEND'  # ➕📜
TT_KEYWORD_REMOVE = 'KEYWORD_REMOVE'  # ➖📜
TT_KEYWORD_GET_AT = 'KEYWORD_GET_AT'  # 🎯 (NOVO)

# --- System (Keywords) ---
TT_KEYWORD_IMPORT = 'KEYWORD_IMPORT'  # ⚙️
TT_KEYWORD_SAVE = 'KEYWORD_SAVE'      # 💾
TT_KEYWORD_SLEEP = 'KEYWORD_SLEEP'    # ⏱️
TT_KEYWORD_READ_FILE = 'KEYWORD_READ_FILE'    # 📖 (NOVO)
TT_KEYWORD_APPEND_FILE = 'KEYWORD_APPEND_FILE'  # ✍️ (NOVO)


################################################################################
# 3. EMOJI MAPPING
# Maps the emoji character to its corresponding token TYPE.
################################################################################

EMOJI_KEYWORDS = {
    # Structure
    '🌱': TT_PROGRAM_START,
    '🌳': TT_PROGRAM_END,

    # Blocks
    '📦': TT_BLOCK_START,
    '📦⛔': TT_BLOCK_END,

    # Variables
    '🔢': TT_KEYWORD_INT,
    '👽': TT_KEYWORD_REAL,
    '💬': TT_KEYWORD_STRING,

    # I/O
    '👀': TT_KEYWORD_READ,
    '🖨️': TT_KEYWORD_PRINT,

    # Math
    '➕': TT_OP_PLUS,
    '➖': TT_OP_MINUS,
    '✖️': TT_OP_MUL,
    '➗': TT_OP_DIV,

    # Assignment
    '👉': TT_ASSIGN,

    # Syntax
    '💭': TT_COMMENT,
    '🔚': TT_END_STATEMENT,

    # Conditionals
    '🤔': TT_KEYWORD_IF,
    '🔀': TT_KEYWORD_ELIF,
    '🤨': TT_KEYWORD_ELSE,

    # Functions
    '🧩': TT_KEYWORD_FUN,
    '🔙': TT_KEYWORD_RETURN,
    '📞': TT_KEYWORD_CALL,       # (NOVO)

    # Loops (NOVO)
    '⏳': TT_KEYWORD_WHILE,
    '🚶': TT_KEYWORD_FOR,

    # Logic
    '⚖️': TT_COMP_EQ,
    '⬆️': TT_COMP_GT,
    '⬇️': TT_COMP_LT,
    '🚫': TT_LOGIC_NOT,
    '🤝': TT_LOGIC_AND,          # (NOVO)
    '🌀': TT_LOGIC_OR,           # (NOVO)

    # Lists
    '📜': TT_KEYWORD_LIST,
    '➕📜': TT_KEYWORD_APPEND,
    '➖📜': TT_KEYWORD_REMOVE,
    '🎯': TT_KEYWORD_GET_AT,       # (NOVO)

    # System
    '⚙️': TT_KEYWORD_IMPORT,
    '💾': TT_KEYWORD_SAVE,
    '⏱️': TT_KEYWORD_SLEEP,
    '📖': TT_KEYWORD_READ_FILE,    # (NOVO)
    '✍️': TT_KEYWORD_APPEND_FILE,  # (NOVO)
}