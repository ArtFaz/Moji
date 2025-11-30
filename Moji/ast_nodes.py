# moji/ast_nodes.py

"""
Defines all the "Node" classes that make up
the Abstract Syntax Tree (AST).

The AST is the hierarchical representation of the source code,
created by the Parser and read by the Interpreter.
"""

################################################################################
# 1. BASE NODES
################################################################################

class Node:
    """ Base class for all AST nodes. """
    def __repr__(self):
        return f'({self.__class__.__name__})'

class ProgramNode(Node):
    """ Root node of the AST. Represents the entire program. """
    def __init__(self, statements):
        self.statements = statements # A list of statement nodes

    def __repr__(self):
        return f'ProgramNode(\n  {self.statements}\n)'

class BlockNode(Node):
    """ Represents a code block 📦 ... 📦⛔. """
    def __init__(self, statements):
        self.statements = statements # A list of statement nodes

    def __repr__(self):
        return f'BlockNode(\n  {self.statements}\n)'

################################################################################
# 2. EXPRESSION NODES (Things that have a value)
################################################################################

class NumberNode(Node):
    """ Represents a numeric literal (Integer or Real). """
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f'Number({self.value})'

class StringNode(Node):
    """ Represents a string literal. """
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f'String("{self.value}")'

class VarAccessNode(Node):
    """ Represents accessing (reading) a variable. """
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.var_name = var_name_token.value

    def __repr__(self):
        return f'VarAccess({self.var_name})'

class BinOpNode(Node):
    """ Represents a binary operation (e.g., 1 ➕ 2, x ⚖️ 10). """
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node} {self.op_token.type} {self.right_node})'

class UnaryOpNode(Node):
    """ Represents a unary operation (e.g., 🚫 x). """
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token.type} {self.node})'

class FuncCallNode(Node):
    """ Represents a function call (e.g., 📞 myFunc arg1 arg2). """
    def __init__(self, node_to_call, arg_nodes):
        # node_to_call is usually a VarAccessNode (the function name)
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes # List of expression nodes

    def __repr__(self):
        return f'Call({self.node_to_call} with {self.arg_nodes})'

class ListAccessNode(Node): # (NOVO)
    """ Represents accessing a list index (e.g., myList 🎯 0). """
    def __init__(self, list_node, index_node):
        self.list_node = list_node
        self.index_node = index_node

    def __repr__(self):
        return f'ListAccess({self.list_node} at {self.index_node})'

class FileReadNode(Node): # (NOVO)
    """ Represents reading a file (e.g., 📖 "data.txt"). """
    def __init__(self, filename_node):
        self.filename_node = filename_node

    def __repr__(self):
        return f'FileRead({self.filename_node})'

class TypeCastNode(Node): # (NOVO)
    """ Represents type conversion (e.g., 🔢 "123"). """
    def __init__(self, type_token, expression_node):
        self.type_token = type_token
        self.expression_node = expression_node

    def __repr__(self):
        return f'Cast(to {self.type_token.type} value: {self.expression_node})'


################################################################################
# 3. STATEMENT NODES (Things that perform an action)
################################################################################

class VarDeclareNode(Node):
    """
    Variable declaration (e.g., 🔢 x 🔚 or 🔢 x 👉 10 🔚).
    """
    def __init__(self, var_type_token, var_name_token, value_node=None):
        self.var_type_token = var_type_token
        self.var_name_token = var_name_token
        self.value_node = value_node # Expression node (e.g., NumberNode) or None

    def __repr__(self):
        if self.value_node:
            return f'Declare({self.var_name_token.value} as {self.var_type_token.type} = {self.value_node})'
        return f'Declare({self.var_name_token.value} as {self.var_type_token.type})'

class VarAssignNode(Node):
    """ Variable re-assignment (e.g., x 👉 20 🔚). """
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.var_name = var_name_token.value
        self.value_node = value_node # Expression node

    def __repr__(self):
        return f'Assign({self.var_name} = {self.value_node})'

class PrintNode(Node):
    """ Print statement 🖨️. """
    def __init__(self, node_to_print):
        self.node_to_print = node_to_print # Expression node

    def __repr__(self):
        return f'Print({self.node_to_print})'

class ReadNode(Node):
    """ Read statement 👀. """
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.var_name = var_name_token.value

    def __repr__(self):
        return f'Read({self.var_name})'

class IfNode(Node):
    """ Conditional statement 🤔 ... 🔀 ... 🤨. """
    def __init__(self, cases, else_case):
        # cases is a list of tuples: [(condition_node, block_node), ...]
        self.cases = cases
        # else_case is a BlockNode or None
        self.else_case = else_case

    def __repr__(self):
        return f'If(Cases: {self.cases}, Else: {self.else_case})'

class WhileNode(Node): # (NOVO)
    """ While loop statement ⏳. """
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node # A BlockNode

    def __repr__(self):
        return f'While({self.condition_node} do {self.body_node})'

class ForNode(Node): # (NOVO)
    """ For-each loop statement 🚶. """
    def __init__(self, var_name_token, list_node, body_node):
        self.var_name_token = var_name_token # Identifier token for the item
        self.list_node = list_node # Expression node (the list to iterate)
        self.body_node = body_node # A BlockNode

    def __repr__(self):
        return f'For(each {self.var_name_token.value} in {self.list_node} do {self.body_node})'

class FuncDefNode(Node):
    """ Function definition 🧩. """
    def __init__(self, func_name_token, arg_name_tokens, body_node):
        self.func_name_token = func_name_token
        self.func_name = func_name_token.value
        self.arg_name_tokens = arg_name_tokens # List of Identifier tokens
        self.body_node = body_node # A BlockNode

    def __repr__(self):
        return f'FuncDef({self.func_name} args: {self.arg_name_tokens})'

class ReturnNode(Node):
    """ Return statement 🔙. """
    def __init__(self, node_to_return):
        # node_to_return is an expression node or None
        self.node_to_return = node_to_return

    def __repr__(self):
        return f'Return({self.node_to_return})'

class ListAppendNode(Node):
    """ List append statement ➕📜. """
    def __init__(self, list_var_token, value_node):
        self.list_var_token = list_var_token
        self.value_node = value_node

    def __repr__(self):
        return f'Append(to {self.list_var_token.value} value: {self.value_node})'

class ListRemoveNode(Node):
    """ List remove statement ➖📜. """
    def __init__(self, list_var_token, index_node):
        self.list_var_token = list_var_token
        self.index_node = index_node # Expression node (the index)

    def __repr__(self):
        return f'Remove(from {self.list_var_token.value} at: {self.index_node})'

class ImportNode(Node):
    """ Import statement ⚙️. """
    def __init__(self, module_name_token):
        self.module_name_token = module_name_token

    def __repr__(self):
        return f'Import({self.module_name_token.value})'

class SaveNode(Node):
    """ Save statement 💾. """
    def __init__(self, data_node, filename_node):
        self.data_node = data_node
        self.filename_node = filename_node

    def __repr__(self):
        return f'Save({self.data_node} to {self.filename_node})'

class FileAppendNode(Node): # (NOVO)
    """ File append statement ✍️. """
    def __init__(self, data_node, filename_node):
        self.data_node = data_node
        self.filename_node = filename_node

    def __repr__(self):
        return f'FileAppend({self.data_node} to {self.filename_node})'

class SleepNode(Node):
    """ Sleep statement ⏱️. """
    def __init__(self, duration_node):
        self.duration_node = duration_node

    def __repr__(self):
        return f'Sleep({self.duration_node})'