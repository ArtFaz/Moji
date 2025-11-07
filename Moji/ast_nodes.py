# moji/ast_nodes.py

"""
Define todas as classes de "Nós" (Nodes) que compõem
a Árvore Sintática Abstrata (AST).

A AST é a representação hierárquica do código-fonte,
criada pelo Parser e lida pelo Interpreter.
"""

################################################################################
# 1. NÓS BASE
################################################################################

class Node:
    """ Classe base para todos os nós da AST. """
    def __repr__(self):
        return f'({self.__class__.__name__})'

class ProgramNode(Node):
    """ Nó raiz da AST. Representa o programa inteiro. """
    def __init__(self, statements):
        self.statements = statements # Uma lista de nós de comando

    def __repr__(self):
        return f'ProgramNode(\n  {self.statements}\n)'

class BlockNode(Node):
    """ Representa um bloco de código 📦 ... 📦⛔. """
    def __init__(self, statements):
        self.statements = statements # Uma lista de nós de comando

    def __repr__(self):
        return f'BlockNode(\n  {self.statements}\n)'

################################################################################
# 2. NÓS DE EXPRESSÃO (Coisas que têm um valor)
################################################################################

class NumberNode(Node):
    """ Representa um literal numérico (Inteiro ou Real). """
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f'Number({self.value})'

class StringNode(Node):
    """ Representa um literal de string. """
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f'String("{self.value}")'

class VarAccessNode(Node):
    """ Representa o acesso (leitura) a uma variável. """
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.var_name = var_name_token.value

    def __repr__(self):
        return f'VarAccess({self.var_name})'

class BinOpNode(Node):
    """ Representa uma operação binária (ex: 1 ➕ 2, x ⚖️ 10). """
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node} {self.op_token.type} {self.right_node})'

class UnaryOpNode(Node):
    """ Representa uma operação unária (ex: 🚫 x). """
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token.type} {self.node})'

class FuncCallNode(Node):
    """ Representa uma chamada de função (ex: minhaFunc(a, b)). """
    def __init__(self, node_to_call, arg_nodes):
        # node_to_call é geralmente um VarAccessNode (o nome da função)
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes # Lista de nós de expressão

    def __repr__(self):
        return f'Call({self.node_to_call} with {self.arg_nodes})'


################################################################################
# 3. NÓS DE COMANDO (Coisas que realizam uma ação)
################################################################################

class VarDeclareNode(Node):
    """
    Declaração de variável (ex: 🔢 x 🔚 ou 🔢 x 👉 10 🔚).
    """
    def __init__(self, var_type_token, var_name_token, value_node=None):
        self.var_type_token = var_type_token
        self.var_name_token = var_name_token
        self.value_node = value_node # Nó da expressão (ex: NumberNode) ou None

    def __repr__(self):
        if self.value_node:
            return f'Declare({self.var_name_token.value} as {self.var_type_token.type} = {self.value_node})'
        return f'Declare({self.var_name_token.value} as {self.var_type_token.type})'

class VarAssignNode(Node):
    """ Re-atribuição de variável (ex: x 👉 20 🔚). """
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.var_name = var_name_token.value
        self.value_node = value_node # Nó da expressão

    def __repr__(self):
        return f'Assign({self.var_name} = {self.value_node})'

class PrintNode(Node):
    """ Comando de impressão 🖨️. """
    def __init__(self, node_to_print):
        self.node_to_print = node_to_print # Nó da expressão

    def __repr__(self):
        return f'Print({self.node_to_print})'

class ReadNode(Node):
    """ Comando de leitura 👀. """
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.var_name = var_name_token.value

    def __repr__(self):
        return f'Read({self.var_name})'

class IfNode(Node):
    """ Comando condicional 🤔 ... 🔀 ... 🤨. """
    def __init__(self, cases, else_case):
        # cases é uma lista de tuplas: [(condicao_node, bloco_node), (condicao_node, bloco_node), ...]
        self.cases = cases
        # else_case é um BlockNode ou None
        self.else_case = else_case

    def __repr__(self):
        return f'If(Cases: {self.cases}, Else: {self.else_case})'

class FuncDefNode(Node):
    """ Definição de função 🧩. """
    def __init__(self, func_name_token, arg_name_tokens, body_node):
        self.func_name_token = func_name_token
        self.func_name = func_name_token.value
        self.arg_name_tokens = arg_name_tokens # Lista de tokens de Identificador
        self.body_node = body_node # Um BlockNode

    def __repr__(self):
        return f'FuncDef({self.func_name} args: {self.arg_name_tokens})'

class ReturnNode(Node):
    """ Comando de retorno 🔙. """
    def __init__(self, node_to_return):
        # node_to_return é um nó de expressão ou None
        self.node_to_return = node_to_return

    def __repr__(self):
        return f'Return({self.node_to_return})'

class ListAppendNode(Node):
    """ Comando ➕📜 (append). """
    def __init__(self, list_var_token, value_node):
        self.list_var_token = list_var_token
        self.value_node = value_node

    def __repr__(self):
        return f'Append(to {self.list_var_token.value} value: {self.value_node})'

class ListRemoveNode(Node):
    """ Comando ➖📜 (remove). """
    def __init__(self, list_var_token, index_node):
        self.list_var_token = list_var_token
        self.index_node = index_node # Nó da expressão (o índice)

    def __repr__(self):
        return f'Remove(from {self.list_var_token.value} at: {self.index_node})'

class ImportNode(Node):
    """ Comando ⚙️ (import). """
    def __init__(self, module_name_token):
        self.module_name_token = module_name_token

    def __repr__(self):
        return f'Import({self.module_name_token.value})'

class SaveNode(Node):
    """ Comando 💾 (save). """
    def __init__(self, data_node, filename_node):
        self.data_node = data_node
        self.filename_node = filename_node

    def __repr__(self):
        return f'Save({self.data_node} to {self.filename_node})'

class SleepNode(Node):
    """ Comando ⏱️ (sleep). """
    def __init__(self, duration_node):
        self.duration_node = duration_node

    def __repr__(self):
        return f'Sleep({self.duration_node})'