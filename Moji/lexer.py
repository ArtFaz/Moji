# moji/lexer.py

# Import Token definitions and the Emoji map from token.py
from .token import (
    Token, EMOJI_KEYWORDS,
    TT_LIT_INT, TT_LIT_REAL, TT_LIT_STRING,
    TT_IDENTIFIER, TT_EOF
)


################################################################################
# 1. LEXER CLASS
# Responsible for taking the source text and breaking it into a list of Tokens.
################################################################################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0  # Current position in the text
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def error(self, message):
        """ Raises an exception in case of a lexical error. """
        raise Exception(f"Lexical Error: {message}")

    def advance(self):
        """ Moves the `pos` pointer to the next character in the text. """
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None  # Indicates End Of File (EOF)

    def peek(self, n=1):
        """
        Looks 'n' characters ahead (lookahead) without consuming the character.
        Returns None if out of bounds.
        """
        peek_pos = self.pos + n
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        """ Skips whitespace characters (space, tab, newline). """
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        """ Skips an entire line of commentary (everything after '💭'). """
        # Advances past the '💭' emoji
        self.advance()
        # Continues advancing until a newline or EOF is found
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def make_number(self):
        """ Processes a number (integer or real). """
        num_str = ''
        dot_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break  # Second decimal point, stop the loop
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_LIT_INT, int(num_str))
        else:
            return Token(TT_LIT_REAL, float(num_str))

    def make_string(self):
        """ Processes a string literal (between quotes). """
        str_val = ''
        self.advance()  # Skip the initial '"'

        while self.current_char is not None and self.current_char != '"':
            str_val += self.current_char
            self.advance()

        if self.current_char is None:
            self.error("Unterminated string.")

        self.advance()  # Skip the final '"'
        return Token(TT_LIT_STRING, str_val)

    def make_identifier(self):
        """ Processes an identifier (variable/function name). """
        ident_str = ''
        # Names can contain letters, numbers (but not at the start), and underscore
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            ident_str += self.current_char
            self.advance()

        # Since our keywords are emojis, we don't need to check if an
        # identifier is a reserved keyword.
        return Token(TT_IDENTIFIER, ident_str)

    def make_tokens(self):
        """
        The main method. Generates a list of all tokens from the source text.
        """
        tokens = []

        while self.current_char is not None:

            # 1. Skip Whitespace
            if self.current_char in ' \t\n\r':
                self.advance()
                continue

            # 2. Skip Comments
            if self.current_char == '💭':
                self.skip_comment()
                continue

            # 3. Numbers (Integers and Reals)
            if self.current_char.isdigit():
                tokens.append(self.make_number())
                continue

            # 4. Strings
            if self.current_char == '"':
                tokens.append(self.make_string())
                continue

            # 5. Identifiers (Variable names)
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.make_identifier())
                continue

            # 6. Emojis (with Lookahead)

            # --- Lookahead Logic ---
            # First, we try to see if it's a 2-character token
            peeked_char = self.peek()
            if peeked_char is not None:
                two_char_emoji = self.current_char + peeked_char
                if two_char_emoji in EMOJI_KEYWORDS:
                    token_type = EMOJI_KEYWORDS[two_char_emoji]
                    tokens.append(Token(token_type, two_char_emoji))
                    self.advance()  # Advance 1st char
                    self.advance()  # Advance 2nd char
                    continue

            # If it's not a 2-character token, try a 1-character one
            if self.current_char in EMOJI_KEYWORDS:
                token_type = EMOJI_KEYWORDS[self.current_char]
                emoji_val = self.current_char
                tokens.append(Token(token_type, emoji_val))
                self.advance()
                continue

            # 7. Error
            # If it got this far, we don't recognize the character
            self.error(f"Illegal character or unknown emoji: '{self.current_char}'")

        # End of loop, add the End Of File token
        tokens.append(Token(TT_EOF))
        return tokens


################################################################################
# 3. Test Block
# (To run this file directly: python -m moji.lexer)
################################################################################

if __name__ == '__main__':
    # Example code from your "hello_world.moji"
    test_code = """
    🌱 💭 This is a test program!

    💬 myName 👉 "Mojji" 🔚
    🖨️ "Hello, " ➕ myName 🔚

    🔢 x 👉 10 🔚
    🤔 x ⚖️ 10 📦
        🖨️ "x is 10!" 🔚
    📦⛔

    🌳
    """

    print(f"--- Testing Lexer with code: ---\n{test_code}")

    try:
        lexer = Lexer(test_code)
        tokens = lexer.make_tokens()

        print("--- Generated Tokens ---")
        for token in tokens:
            print(token)

    except Exception as e:
        print(f"\n!!! LEXER ERROR: {e}")