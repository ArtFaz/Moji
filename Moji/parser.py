# moji/parser.py

# Imports all nodes that the Parser can build
from .ast_nodes import (
    Node, ProgramNode, BlockNode, NumberNode, StringNode, VarAccessNode,
    BinOpNode, UnaryOpNode, VarDeclareNode, VarAssignNode, PrintNode,
    ReadNode, IfNode, FuncDefNode, ReturnNode, ListAppendNode,
    ListRemoveNode, ImportNode, SaveNode, SleepNode
)
# Imports all token types that the Parser needs to recognize
from .token import (
    TT_PROGRAM_START, TT_PROGRAM_END, TT_BLOCK_START, TT_BLOCK_END,
    TT_KEYWORD_INT, TT_KEYWORD_REAL, TT_KEYWORD_STRING, TT_KEYWORD_LIST,
    TT_KEYWORD_READ, TT_KEYWORD_PRINT, TT_OP_PLUS, TT_OP_MINUS,
    TT_OP_MUL, TT_OP_DIV, TT_ASSIGN, TT_END_STATEMENT, TT_KEYWORD_IF,
    TT_KEYWORD_ELIF, TT_KEYWORD_ELSE, TT_KEYWORD_FUN, TT_KEYWORD_RETURN,
    TT_COMP_EQ, TT_COMP_GT, TT_COMP_LT, TT_LOGIC_NOT, TT_KEYWORD_APPEND,
    TT_KEYWORD_REMOVE, TT_KEYWORD_IMPORT, TT_KEYWORD_SAVE, TT_KEYWORD_SLEEP,
    TT_IDENTIFIER, TT_LIT_INT, TT_LIT_REAL, TT_LIT_STRING, TT_EOF
)


################################################################################
# 1. SYNTAX ERROR
################################################################################

class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__(f"Syntax Error: {message}")


################################################################################
# 2. PARSER CLASS
################################################################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        # Initializes the current token with the first token in the list
        self.current_token = self.tokens[self.token_idx] if self.tokens else None

    def advance(self):
        """ Advances to the next token in the list. """
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            # If no more tokens, current token remains the last one (usually EOF)
            self.current_token = self.tokens[-1]
        return self.current_token

    def peek(self, n=1):
        """ Peeks at the token 'n' positions ahead without advancing. """
        peek_idx = self.token_idx + n
        if peek_idx < len(self.tokens):
            return self.tokens[peek_idx]
        return None

    def eat(self, expected_token_type):
        """
        Consumes the current token if it is of the expected type.
        If not, raises a syntax error.
        """
        if self.current_token.type == expected_token_type:
            self.advance()
        else:
            raise SyntaxError(
                f"Expected '{expected_token_type}', but found '{self.current_token.type}'"
            )

    # --- STARTING POINT (Top Level) ---

    def parse(self):
        """
        Starts the parsing process.
        A program is: 🌱 ...list of statements... 🌳
        """
        self.eat(TT_PROGRAM_START)

        # statements() will read all statements until it finds 🌳
        statements = self.statements(end_token_type=TT_PROGRAM_END)

        # If statements() stopped and it's not 🌳, something is wrong
        self.eat(TT_PROGRAM_END)

        # If it got here and the next token is not EOF, there's leftover code
        if self.current_token.type != TT_EOF:
            raise SyntaxError("Code found after program end '🌳'.")

        return ProgramNode(statements)

    # --- STATEMENTS ---

    def statements(self, end_token_type):
        """
        Processes a list of statements until an end token is found
        (e.g., 🌳 for the program, 📦⛔ for a block).
        """
        statement_list = []

        while self.current_token.type != end_token_type and self.current_token.type != TT_EOF:
            statement_list.append(self.statement())

        return statement_list

    def statement(self):
        """ Router: Decides which type of statement is being read. """
        token_type = self.current_token.type

        # 🖨️ ... 🔚 (Print)
        if token_type == TT_KEYWORD_PRINT:
            return self.print_statement()

        # 👀 ... 🔚 (Read)
        if token_type == TT_KEYWORD_READ:
            return self.read_statement()

        # 🔢, 💬, 👽, 📜 ... (Var Declaration)
        if token_type in (TT_KEYWORD_INT, TT_KEYWORD_REAL, TT_KEYWORD_STRING, TT_KEYWORD_LIST):
            return self.var_declaration()

        # 🤔 ... (If)
        if token_type == TT_KEYWORD_IF:
            return self.if_statement()

        # 📦 ... 📦⛔ (Block)
        if token_type == TT_BLOCK_START:
            return self.block()

        # 🧩 ... (Function Definition)
        if token_type == TT_KEYWORD_FUN:
            return self.func_definition()

        # 🔙 ... (Return)
        if token_type == TT_KEYWORD_RETURN:
            return self.return_statement()

        # ⚙️, 💾, ⏱️ (System Commands)
        if token_type == TT_KEYWORD_IMPORT:
            return self.import_statement()
        if token_type == TT_KEYWORD_SAVE:
            return self.save_statement()
        if token_type == TT_KEYWORD_SLEEP:
            return self.sleep_statement()

        # Identifier (Could be Assignment or List Op)
        if token_type == TT_IDENTIFIER:
            next_token_type = self.peek().type

            # x 👉 ... 🔚 (Assignment)
            if next_token_type == TT_ASSIGN:
                return self.var_assignment()

            # myList ➕📜 ... 🔚 (List Append)
            if next_token_type == TT_KEYWORD_APPEND:
                return self.list_append()

            # myList ➖📜 ... 🔚 (List Remove)
            if next_token_type == TT_KEYWORD_REMOVE:
                return self.list_remove()

        # If it's none of the above, it's an error.
        raise SyntaxError(f"Unexpected statement: token '{self.current_token}'")

    def print_statement(self):
        """ Parses: 🖨️ <expression> 🔚 """
        self.eat(TT_KEYWORD_PRINT)
        node_to_print = self.expression()
        self.eat(TT_END_STATEMENT)
        return PrintNode(node_to_print)

    def read_statement(self):
        """ Parses: 👀 <identifier> 🔚 """
        self.eat(TT_KEYWORD_READ)
        var_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_END_STATEMENT)
        return ReadNode(var_token)

    def var_declaration(self):
        """ Parses: <type> <name> [👉 <expression>] 🔚 """
        type_token = self.current_token
        self.advance()  # Consume the type (🔢, 💬, etc.)

        var_name_token = self.current_token
        self.eat(TT_IDENTIFIER)

        value_node = None
        # Check if it's a declaration with initialization
        if self.current_token.type == TT_ASSIGN:
            self.eat(TT_ASSIGN)
            value_node = self.expression()

        self.eat(TT_END_STATEMENT)
        return VarDeclareNode(type_token, var_name_token, value_node)

    def var_assignment(self):
        """ Parses: <name> 👉 <expression> 🔚 """
        var_name_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_ASSIGN)
        value_node = self.expression()
        self.eat(TT_END_STATEMENT)
        return VarAssignNode(var_name_token, value_node)

    def list_append(self):
        """ Parses: <list_name> ➕📜 <expression> 🔚 """
        list_var_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_KEYWORD_APPEND)
        value_node = self.expression()
        self.eat(TT_END_STATEMENT)
        return ListAppendNode(list_var_token, value_node)

    def list_remove(self):
        """ Parses: <list_name> ➖📜 <index_expression> 🔚 """
        list_var_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_KEYWORD_REMOVE)
        index_node = self.expression()  # The index to be removed
        self.eat(TT_END_STATEMENT)
        return ListRemoveNode(list_var_token, index_node)

    def if_statement(self):
        """ Parses: 🤔 <cond> 📦 ... 📦⛔ [🔀 <cond> 📦 ... 📦⛔]* [🤨 📦 ... 📦⛔] """
        cases = []
        else_case = None

        # IF block (mandatory)
        self.eat(TT_KEYWORD_IF)
        condition = self.expression()
        body = self.block()
        cases.append((condition, body))

        # ELIF blocks (optional)
        while self.current_token.type == TT_KEYWORD_ELIF:
            self.eat(TT_KEYWORD_ELIF)
            condition = self.expression()
            body = self.block()
            cases.append((condition, body))

        # ELSE block (optional)
        if self.current_token.type == TT_KEYWORD_ELSE:
            self.eat(TT_KEYWORD_ELSE)
            else_case = self.block()

        return IfNode(cases, else_case)

    def block(self):
        """ Parses: 📦 <list_of_statements> 📦⛔ """
        self.eat(TT_BLOCK_START)
        # statements() will read everything until it finds 📦⛔
        statements_list = self.statements(end_token_type=TT_BLOCK_END)
        self.eat(TT_BLOCK_END)
        return BlockNode(statements_list)

    def func_definition(self):
        """ Parses: 🧩 <name> [arg1] [arg2] ... 📦 ... 📦⛔ """
        self.eat(TT_KEYWORD_FUN)

        func_name_token = self.current_token
        self.eat(TT_IDENTIFIER)

        arg_name_tokens = []
        # Keep reading argument names until 📦 is found
        while self.current_token.type == TT_IDENTIFIER:
            arg_name_tokens.append(self.current_token)
            self.eat(TT_IDENTIFIER)

        body_node = self.block()
        return FuncDefNode(func_name_token, arg_name_tokens, body_node)

    def return_statement(self):
        """ Parses: 🔙 [<expression>] 🔚 """
        self.eat(TT_KEYWORD_RETURN)

        node_to_return = None
        # If there is something to return (not just "🔙 🔚")
        if self.current_token.type != TT_END_STATEMENT:
            node_to_return = self.expression()

        self.eat(TT_END_STATEMENT)
        return ReturnNode(node_to_return)

    # System commands (simple)
    def import_statement(self):
        self.eat(TT_KEYWORD_IMPORT)
        module_name_token = self.current_token
        self.eat(TT_IDENTIFIER)  # Assuming we import by name
        self.eat(TT_END_STATEMENT)
        return ImportNode(module_name_token)

    def save_statement(self):
        self.eat(TT_KEYWORD_SAVE)
        data_node = self.expression()
        filename_node = self.expression()  # e.g.: 💾 variable "file.txt" 🔚
        self.eat(TT_END_STATEMENT)
        return SaveNode(data_node, filename_node)

    def sleep_statement(self):
        self.eat(TT_KEYWORD_SLEEP)
        duration_node = self.expression()
        self.eat(TT_END_STATEMENT)
        return SleepNode(duration_node)

    # --- EXPRESSIONS (Operator Precedence) ---

    def binary_operation(self, func_to_call, valid_op_types):
        """
        Generic helper function to process binary operations
        (like 1 ➕ 2, or 10 ⚖️ x)
        """
        left = func_to_call()

        while self.current_token.type in valid_op_types:
            op_token = self.current_token
            self.eat(op_token.type)
            right = func_to_call()
            left = BinOpNode(left, op_token, right)

        return left

    def expression(self):
        """ Entry point for any expression. (Lowest precedence level) """
        return self.comparison()

    def comparison(self):
        """ Parses: ⚖️, ⬆️, ⬇️ """
        return self.binary_operation(self.term, (TT_COMP_EQ, TT_COMP_GT, TT_COMP_LT))

    def term(self):
        """ Parses: ➕, ➖ """
        return self.binary_operation(self.factor, (TT_OP_PLUS, TT_OP_MINUS))

    def factor(self):
        """ Parses: ✖️, ➗ """
        return self.binary_operation(self.unary, (TT_OP_MUL, TT_OP_DIV))

    def unary(self):
        """ Parses: 🚫 """
        if self.current_token.type == TT_LOGIC_NOT:
            op_token = self.current_token
            self.eat(TT_LOGIC_NOT)
            node = self.unary()  # Recursive call to allow '🚫🚫x'
            return UnaryOpNode(op_token, node)
        return self.atom()

    def atom(self):
        """
        Processes the "atoms" of the grammar: numbers, strings, var names.
        (Highest precedence level).
        """
        token = self.current_token

        if token.type == TT_LIT_INT or token.type == TT_LIT_REAL:
            self.eat(token.type)
            return NumberNode(token)

        elif token.type == TT_LIT_STRING:
            self.eat(TT_LIT_STRING)
            return StringNode(token)

        elif token.type == TT_IDENTIFIER:
            self.eat(TT_IDENTIFIER)
            return VarAccessNode(token)  # Accessing a variable

        # If it's none of the above, it's a syntax error in the expression
        raise SyntaxError(f"Expected an Integer, Real, String, or Identifier, but found: {token}")


################################################################################
# 3. Test Block
# (To run this file directly: python -m moji.parser)
################################################################################

if __name__ == '__main__':
    # We need the Lexer to generate tokens first
    from .lexer import Lexer

    # Example code from your "hello_world.moji"
    test_code = """
    🌱 💭 This is a test program!

    💬 myName 👉 "Moji" 🔚
    🖨️ "Hello, " ➕ myName 🔚

    🔢 x 👉 10 🔚
    🤔 x ⚖️ 10 📦
        🖨️ "x is 10!" 🔚
    📦⛔

    🌳
    """

    print(f"--- Testing Parser with code: ---\n{test_code}")

    try:
        # 1. Lexer
        lexer = Lexer(test_code)
        tokens = lexer.make_tokens()
        print("--- Generated Tokens (by Lexer) ---")
        for t in tokens:
            print(t)

        # 2. Parser
        parser = Parser(tokens)
        ast = parser.parse()

        print("\n--- Generated AST (by Parser) ---")
        print(ast)

    except Exception as e:
        print(f"\n!!! PARSER ERROR: {e}")