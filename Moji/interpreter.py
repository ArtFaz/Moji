# moji/interpreter.py

import time

# Importa todos os nós, pois o interpretador precisa saber como "visitar" cada um
from .ast_nodes import *
# Importa os tipos de token para checagem (ex: tipo de operação)
from .token import (
    TT_OP_PLUS, TT_OP_MINUS, TT_OP_MUL, TT_OP_DIV,
    TT_COMP_EQ, TT_COMP_GT, TT_COMP_LT, TT_LOGIC_NOT,
    TT_KEYWORD_INT, TT_KEYWORD_REAL, TT_KEYWORD_STRING, TT_KEYWORD_LIST
)


################################################################################
# 1. ERRO DE EXECUÇÃO
################################################################################

class RuntimeError(Exception):
    def __init__(self, message):
        # Erros que acontecem durante a *execução* do código Mojji
        super().__init__(f"Erro de Execução: {message}")


################################################################################
# 2. CLASSE INTERPRETER
################################################################################

class Interpreter:
    def __init__(self):
        # A Tabela de Símbolos (memória) que armazena as variáveis
        self.symbol_table = {}

    def visit(self, node):
        """
        O "roteador" principal.
        Chama o método 'visit_NODE' específico com base no tipo do nó.
        Ex: Se 'node' é um 'PrintNode', ele chama 'self.visit_PrintNode(node)'
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        """ Método de fallback se um 'visit_' não for implementado. """
        raise RuntimeError(f"Nenhum método 'visit_{type(node).__name__}' definido")

    def run(self, ast):
        """ Ponto de entrada público para executar a AST. """
        try:
            return self.visit(ast)
        except RuntimeError as e:
            print(e)

    # --- NÓS DE "FOLHA" (que retornam valores) ---

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_VarAccessNode(self, node):
        """ Lê um valor da tabela de símbolos. """
        var_name = node.var_name
        value = self.symbol_table.get(var_name)

        if value is None:
            raise RuntimeError(f"Variável '{var_name}' não foi definida.")

        return value

    # --- NÓS DE OPERAÇÃO (que calculam valores) ---

    def visit_BinOpNode(self, node):
        """ Executa operações binárias (ex: 1 ➕ 2, x ⚖️ 10). """
        left_val = self.visit(node.left_node)
        right_val = self.visit(node.right_node)
        op_type = node.op_token.type

        # Operações Matemáticas
        if op_type == TT_OP_PLUS:
            # *** INÍCIO DA CORREÇÃO ***
            # Se um dos lados for string, força a concatenação
            if isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
            # Senão, é adição numérica
            return left_val + right_val
            # *** FIM DA CORREÇÃO ***

        elif op_type == TT_OP_MINUS:
            return left_val - right_val
        elif op_type == TT_OP_MUL:
            return left_val * right_val
        elif op_type == TT_OP_DIV:
            if right_val == 0:
                raise RuntimeError("Divisão por zero.")
            return left_val / right_val

        # Operações de Comparação
        elif op_type == TT_COMP_EQ:
            return left_val == right_val
        elif op_type == TT_COMP_GT:
            return left_val > right_val
        elif op_type == TT_COMP_LT:
            return left_val < right_val

        raise RuntimeError(f"Operador binário desconhecido: {op_type}")

    def visit_UnaryOpNode(self, node):
        """ Executa operações unárias (ex: 🚫 x). """
        op_type = node.op_token.type
        value = self.visit(node.node)

        if op_type == TT_LOGIC_NOT:
            return not value  # Negação booleana do Python

        raise RuntimeError(f"Operador unário desconhecido: {op_type}")

    # --- NÓS DE COMANDO (Statements) ---

    def visit_ProgramNode(self, node):
        """ Executa cada comando do programa. """
        for statement in node.statements:
            self.visit(statement)  # Não esperamos retorno

    def visit_BlockNode(self, node):
        """ Executa cada comando de um bloco. """
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDeclareNode(self, node):
        """ Cria uma nova variável na tabela de símbolos. """
        var_name = node.var_name_token.value

        if var_name in self.symbol_table:
            raise RuntimeError(f"Variável '{var_name}' já foi declarada.")

        # Se um valor foi fornecido (ex: 🔢 x 👉 10)
        if node.value_node:
            value = self.visit(node.value_node)
        else:
            # Se não, usa um valor padrão baseado no tipo
            if node.var_type_token.type == TT_KEYWORD_INT:
                value = 0
            elif node.var_type_token.type == TT_KEYWORD_REAL:
                value = 0.0
            elif node.var_type_token.type == TT_KEYWORD_STRING:
                value = ""
            elif node.var_type_token.type == TT_KEYWORD_LIST:
                value = []
            else:
                value = None  # Tipo desconhecido?

        self.symbol_table[var_name] = value

    def visit_VarAssignNode(self, node):
        """ Atualiza o valor de uma variável existente. """
        var_name = node.var_name

        if var_name not in self.symbol_table:
            raise RuntimeError(f"Variável '{var_name}' não foi declarada. Use 🔢, 💬, etc. para declarar.")

        value = self.visit(node.value_node)
        self.symbol_table[var_name] = value

    def visit_PrintNode(self, node):
        """ Imprime um valor no console. """
        value_to_print = self.visit(node.node_to_print)
        print(value_to_print)

    def visit_ReadNode(self, node):
        """ Lê um input do usuário e salva na variável. """
        var_name = node.var_name

        if var_name not in self.symbol_table:
            raise RuntimeError(f"Variável '{var_name}' não declarada. Impossível ler (read).")

        # Pega o tipo *atual* da variável para tentar converter o input
        current_value = self.symbol_table[var_name]
        input_str = input(f"Digite o valor para {var_name}: ")

        try:
            if isinstance(current_value, int):
                new_value = int(input_str)
            elif isinstance(current_value, float):
                new_value = float(input_str)
            else:
                # Se for String, Lista, etc., apenas salva a string
                new_value = input_str
        except ValueError:
            raise RuntimeError(f"Input inválido. Esperava um tipo compatível com o de '{var_name}'.")

        self.symbol_table[var_name] = new_value

    def visit_IfNode(self, node):
        """ Executa blocos condicionais (If/Elif/Else). """
        # Itera sobre os blocos 'IF' e 'ELIF'
        for condition_node, body_node in node.cases:
            condition_value = self.visit(condition_node)

            if condition_value:  # Se a condição for Verdadeira (True)
                self.visit(body_node)
                return  # Para de checar (só executa um bloco)

        # Se nenhum 'IF/ELIF' foi verdadeiro, checa o 'ELSE'
        if node.else_case:
            self.visit(node.else_case)

    # --- COMANDOS DE LISTA ---

    def visit_ListAppendNode(self, node):
        list_name = node.list_var_token.value
        list_obj = self.symbol_table.get(list_name)

        if list_obj is None:
            raise RuntimeError(f"Variável de lista '{list_name}' não encontrada.")
        if not isinstance(list_obj, list):
            raise RuntimeError(f"'{list_name}' não é uma lista. Impossível usar ➕📜.")

        value_to_append = self.visit(node.value_node)
        list_obj.append(value_to_append)

    def visit_ListRemoveNode(self, node):
        list_name = node.list_var_token.value
        list_obj = self.symbol_table.get(list_name)

        if not isinstance(list_obj, list):
            raise RuntimeError(f"'{list_name}' não é uma lista. Impossível usar ➖📜.")

        index_to_remove = self.visit(node.index_node)
        if not isinstance(index_to_remove, int):
            raise RuntimeError("Índice para remover (➖📜) deve ser um inteiro.")

        try:
            list_obj.pop(index_to_remove)
        except IndexError:
            raise RuntimeError(f"Índice {index_to_remove} fora do range da lista '{list_name}'.")

    # --- COMANDOS DE SISTEMA ---

    def visit_SaveNode(self, node):
        """ 💾 <dado> <nome_arquivo> 🔚 """
        data = self.visit(node.data_node)
        filename = self.visit(node.filename_node)

        if not isinstance(filename, str):
            raise RuntimeError("Nome do arquivo para 💾 (Salvar) deve ser uma string.")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(data))
        except Exception as e:
            raise RuntimeError(f"Falha ao salvar arquivo: {e}")

    def visit_SleepNode(self, node):
        """ ⏱️ <duração> 🔚 """
        duration = self.visit(node.duration_node)

        try:
            time.sleep(float(duration))
        except (ValueError, TypeError):
            raise RuntimeError("Duração para ⏱️ (Sleep) deve ser um número (int ou real).")

    # --- AINDA NÃO IMPLEMENTADOS (Funções, Imports) ---

    def visit_FuncDefNode(self, node):
        # O Parser cria este nó, mas chamadas de função não estão implementadas no Parser
        raise NotImplementedError("Definição de função 🧩 não está completamente implementada.")

    def visit_ReturnNode(self, node):
        raise NotImplementedError("Retorno 🔙 não está implementado.")

    def visit_ImportNode(self, node):
        raise NotImplementedError("Import ⚙️ não está implementado.")


################################################################################
# 3. Bloco de Teste
################################################################################

if __name__ == '__main__':
    # Importa as classes necessárias para o teste
    from .lexer import Lexer
    from .parser import Parser, SyntaxError

    test_code = """
    🌱 💭 Este é um programa de teste completo!

    💬 meuNome 👉 "Moji" 🔚
    🖨️ "Olá, " ➕ meuNome 🔚

    🔢 x 👉 10 🔚
    🤔 x ⚖️ 10 📦
        🖨️ "x é 10!" 🔚
    📦⛔

    🖨️ "--- Teste de Input/Output ---" 🔚
    🔢 idade 🔚
    👀 idade 🔚
    🖨️ "Sua idade é: " ➕ idade 🔚

    💾 "Este é um teste" "teste.txt" 🔚

    🌳
    """

    print(f"--- Executando Código Mojji: ---\n{test_code}")
    print("--- Início da Execução ---")

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
        print(f"\n!!! ERRO DE SINTAXE: {e}")
    except RuntimeError as e:
        print(f"\n!!! ERRO DE EXECUÇÃO: {e}")
    except Exception as e:
        print(f"\n!!! ERRO INESPERADO: {e}")

    print("--- Fim da Execução ---")