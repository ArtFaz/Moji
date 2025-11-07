# moji/interpreter.py

import time

# Import all nodes, as the interpreter needs to know how to "visit" each one
from .ast_nodes import *
# Import token types for checking (e.g., operation type)
from .token import (
    TT_OP_PLUS, TT_OP_MINUS, TT_OP_MUL, TT_OP_DIV,
    TT_COMP_EQ, TT_COMP_GT, TT_COMP_LT, TT_LOGIC_NOT,
    TT_KEYWORD_INT, TT_KEYWORD_REAL, TT_KEYWORD_STRING, TT_KEYWORD_LIST
)


################################################################################
# 1. RUNTIME ERROR
################################################################################

class RuntimeError(Exception):
    def __init__(self, message):
        # Errors that happen during the *execution* of Moji code
        super().__init__(f"Runtime Error: {message}")


################################################################################
# 2. INTERPRETER CLASS
################################################################################

class Interpreter:
    def __init__(self):
        # The Symbol Table (memory) that stores variables
        self.symbol_table = {}

    def visit(self, node):
        """
        The main "router".
        Calls the specific 'visit_NODE' method based on the node's type.
        E.g.: If 'node' is a 'PrintNode', it calls 'self.visit_PrintNode(node)'
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        """ Fallback method if a 'visit_' is not implemented. """
        raise RuntimeError(f"No 'visit_{type(node).__name__}' method defined")

    def run(self, ast):
        """ Public entry point to execute the AST. """
        try:
            return self.visit(ast)
        except RuntimeError as e:
            print(e)

    # --- "LEAF" NODES (that return values) ---

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_VarAccessNode(self, node):
        """ Reads a value from the symbol table. """
        var_name = node.var_name
        value = self.symbol_table.get(var_name)

        if value is None:
            raise RuntimeError(f"Variable '{var_name}' has not been defined.")

        return value

    # --- OPERATION NODES (that calculate values) ---

    def visit_BinOpNode(self, node):
        """ Executes binary operations (e.g., 1 ➕ 2, x ⚖️ 10). """
        left_val = self.visit(node.left_node)
        right_val = self.visit(node.right_node)
        op_type = node.op_token.type

        # Mathematical Operations
        if op_type == TT_OP_PLUS:
            # If one side is a string, force concatenation
            if isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
            # Otherwise, it's numeric addition
            return left_val + right_val

        elif op_type == TT_OP_MINUS:
            return left_val - right_val
        elif op_type == TT_OP_MUL:
            return left_val * right_val
        elif op_type == TT_OP_DIV:
            if right_val == 0:
                raise RuntimeError("Division by zero.")
            return left_val / right_val

        # Comparison Operations
        elif op_type == TT_COMP_EQ:
            return left_val == right_val
        elif op_type == TT_COMP_GT:
            return left_val > right_val
        elif op_type == TT_COMP_LT:
            return left_val < right_val

        raise RuntimeError(f"Unknown binary operator: {op_type}")

    def visit_UnaryOpNode(self, node):
        """ Executes unary operations (e.g., 🚫 x). """
        op_type = node.op_token.type
        value = self.visit(node.node)

        if op_type == TT_LOGIC_NOT:
            return not value  # Python's boolean negation

        raise RuntimeError(f"Unknown unary operator: {op_type}")

    # --- STATEMENT NODES ---

    def visit_ProgramNode(self, node):
        """ Executes each statement in the program. """
        for statement in node.statements:
            self.visit(statement)  # We don't expect a return value

    def visit_BlockNode(self, node):
        """ Executes each statement in a block. """
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDeclareNode(self, node):
        """ Creates a new variable in the symbol table. """
        var_name = node.var_name_token.value

        if var_name in self.symbol_table:
            raise RuntimeError(f"Variable '{var_name}' has already been declared.")

        # If a value was provided (e.g., 🔢 x 👉 10)
        if node.value_node:
            value = self.visit(node.value_node)
        else:
            # Otherwise, use a default value based on the type
            if node.var_type_token.type == TT_KEYWORD_INT:
                value = 0
            elif node.var_type_token.type == TT_KEYWORD_REAL:
                value = 0.0
            elif node.var_type_token.type == TT_KEYWORD_STRING:
                value = ""
            elif node.var_type_token.type == TT_KEYWORD_LIST:
                value = []
            else:
                value = None  # Unknown type?

        self.symbol_table[var_name] = value

    def visit_VarAssignNode(self, node):
        """ Updates the value of an existing variable. """
        var_name = node.var_name

        if var_name not in self.symbol_table:
            raise RuntimeError(f"Variable '{var_name}' not declared. Use 🔢, 💬, etc. to declare.")

        value = self.visit(node.value_node)
        self.symbol_table[var_name] = value

    def visit_PrintNode(self, node):
        """ Prints a value to the console. """
        value_to_print = self.visit(node.node_to_print)
        print(value_to_print)

    def visit_ReadNode(self, node):
        """ Reads user input and saves it to the variable. """
        var_name = node.var_name

        if var_name not in self.symbol_table:
            raise RuntimeError(f"Variable '{var_name}' not declared. Cannot read.")

        # Get the *current* type of the variable to try converting the input
        current_value = self.symbol_table[var_name]
        input_str = input(f"Enter value for {var_name}: ")

        try:
            if isinstance(current_value, int):
                new_value = int(input_str)
            elif isinstance(current_value, float):
                new_value = float(input_str)
            else:
                # If it's String, List, etc., just save the string
                new_value = input_str
        except ValueError:
            raise RuntimeError(f"Invalid input. Expected a type compatible with '{var_name}'.")

        self.symbol_table[var_name] = new_value

    def visit_IfNode(self, node):
        """ Executes conditional blocks (If/Elif/Else). """
        # Iterate over 'IF' and 'ELIF' blocks
        for condition_node, body_node in node.cases:
            condition_value = self.visit(condition_node)

            if condition_value:  # If the condition is True
                self.visit(body_node)
                return  # Stop checking (only execute one block)

        # If no 'IF/ELIF' was true, check 'ELSE'
        if node.else_case:
            self.visit(node.else_case)

    # --- LIST COMMANDS ---

    def visit_ListAppendNode(self, node):
        list_name = node.list_var_token.value
        list_obj = self.symbol_table.get(list_name)

        if list_obj is None:
            raise RuntimeError(f"List variable '{list_name}' not found.")
        if not isinstance(list_obj, list):
            raise RuntimeError(f"'{list_name}' is not a list. Cannot use ➕📜.")

        value_to_append = self.visit(node.value_node)
        list_obj.append(value_to_append)

    def visit_ListRemoveNode(self, node):
        list_name = node.list_var_token.value
        list_obj = self.symbol_table.get(list_name)

        if not isinstance(list_obj, list):
            raise RuntimeError(f"'{list_name}' is not a list. Cannot use ➖📜.")

        index_to_remove = self.visit(node.index_node)
        if not isinstance(index_to_remove, int):
            raise RuntimeError("Index for removal (➖📜) must be an integer.")

        try:
            list_obj.pop(index_to_remove)
        except IndexError:
            raise RuntimeError(f"Index {index_to_remove} out of range for list '{list_name}'.")

    # --- SYSTEM COMMANDS ---

    def visit_SaveNode(self, node):
        """ 💾 <data> <filename> 🔚 """
        data = self.visit(node.data_node)
        filename = self.visit(node.filename_node)

        if not isinstance(filename, str):
            raise RuntimeError("Filename for 💾 (Save) must be a string.")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(data))
        except Exception as e:
            raise RuntimeError(f"Failed to save file: {e}")

    def visit_SleepNode(self, node):
        """ ⏱️ <duration> 🔚 """
        duration = self.visit(node.duration_node)

        try:
            time.sleep(float(duration))
        except (ValueError, TypeError):
            raise RuntimeError("Duration for ⏱️ (Sleep) must be a number (int or real).")

    # --- NOT YET IMPLEMENTED (Functions, Imports) ---

    def visit_FuncDefNode(self, node):
        # The Parser creates this node, but function calls are not implemented.
        raise NotImplementedError("Function definition 🧩 is not fully implemented.")

    def visit_ReturnNode(self, node):
        raise NotImplementedError("Return 🔙 is not implemented.")

    def visit_ImportNode(self, node):
        raise NotImplementedError("Import ⚙️ is not implemented.")


################################################################################
# 3. Test Block
################################################################################

if __name__ == '__main__':
    # Import necessary classes for testing
    from .lexer import Lexer
    from .parser import Parser, SyntaxError

    test_code = """
    🌱 💭 This is a complete test program!

    💬 myName 👉 "Moji" 🔚
    🖨️ "Hello, " ➕ myName 🔚

    🔢 x 👉 10 🔚
    🤔 x ⚖️ 10 📦
        🖨️ "x is 10!" 🔚
    📦⛔

    🖨️ "--- Input/Output Test ---" 🔚
    🔢 age 🔚
    👀 age 🔚
    🖨️ "Your age is: " ➕ age 🔚

    💾 "This is a test" "test.txt" 🔚

    🌳
    """

    print(f"--- Executing Moji Code: ---\n{test_code}")
    print("--- Execution Start ---")

    try:
        # 1. Lexer
        lexer = Lexer(test_code)
        tokens = lexer.make_tokens()

        # 2. Parser
        parser = Parser(tokens)
        ast = parser.parse()

        # 3. Interpreter
        interpreter = Interpreter()
        interpreter.run(ast)

    except SyntaxError as e:
        print(f"\n!!! SYNTAX ERROR: {e}")
    except RuntimeError as e:
        print(f"\n!!! RUNTIME ERROR: {e}")
    except Exception as e:
        print(f"\n!!! UNEXPECTED ERROR: {e}")

    print("--- Execution End ---")