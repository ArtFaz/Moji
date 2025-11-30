# moji/interpreter.py

import time

# Import all nodes, as the interpreter needs to know how to "visit" each one
from .ast_nodes import *
# Import token types for checking (e.g., operation type)
from .token import (
    TT_OP_PLUS, TT_OP_MINUS, TT_OP_MUL, TT_OP_DIV,
    TT_COMP_EQ, TT_COMP_GT, TT_COMP_LT, TT_LOGIC_NOT,
    TT_KEYWORD_INT, TT_KEYWORD_REAL, TT_KEYWORD_STRING, TT_KEYWORD_LIST,
    # (NOVOS TOKENS)
    TT_LOGIC_AND, TT_LOGIC_OR
)


################################################################################
# 1. RUNTIME ERROR & RETURN SIGNAL
################################################################################

class RuntimeError(Exception):
    def __init__(self, message):
        # Errors that happen during the *execution* of Moji code
        super().__init__(f"Runtime Error: {message}")


class ReturnSignal(Exception):  # (NOVO)
    """
    Uma exceção especial usada para "pular" para fora da execução de uma
    função quando o comando 🔙 (return) é encontrado.
    """

    def __init__(self, value):
        self.value = value


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
        # (ATUALIZADO) Captura o ReturnSignal no nível superior (não deve acontecer)
        except ReturnSignal:
            raise RuntimeError("Comando '🔙' (Return) encontrado fora de uma função 🧩.")
        except RuntimeError as e:
            # Erros de runtime já formatados
            raise e
        except Exception as e:
            # Erros inesperados do Python
            raise RuntimeError(f"Erro interno do Moji: {e}")

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
            raise RuntimeError(f"Variável '{var_name}' não foi definida.")

        return value

    def visit_ListAccessNode(self, node):  # (NOVO)
        """ 🎯 (Acessar Índice) - Retorna um item da lista. """
        list_val = self.visit(node.list_node)
        index_val = self.visit(node.index_node)

        if not isinstance(list_val, list):
            raise RuntimeError(f"Não é possível usar 🎯 (acessar índice) em algo que não é uma lista 📜.")

        if not isinstance(index_val, int):
            raise RuntimeError(f"Índice para 🎯 (acessar índice) deve ser um inteiro 🔢.")

        try:
            return list_val[index_val]
        except IndexError:
            raise RuntimeError(f"Índice {index_val} fora do alcance para a lista.")

    def visit_FileReadNode(self, node):  # (NOVO)
        """ 📖 (Ler Arquivo) - Retorna o conteúdo do arquivo. """
        filename = self.visit(node.filename_node)
        if not isinstance(filename, str):
            raise RuntimeError(f"Nome do arquivo para 📖 (Ler) deve ser uma string 💬.")

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo '{filename}' não encontrado.")
        except Exception as e:
            raise RuntimeError(f"Erro ao ler o arquivo '{filename}': {e}")

    def visit_TypeCastNode(self, node):  # (NOVO)
        """ 🔢/👽/💬 (Converter Tipo) - Retorna o valor convertido. """
        value_to_cast = self.visit(node.expression_node)
        target_type = node.type_token.type

        try:
            if target_type == TT_KEYWORD_INT:
                return int(value_to_cast)
            elif target_type == TT_KEYWORD_REAL:
                return float(value_to_cast)
            elif target_type == TT_KEYWORD_STRING:
                return str(value_to_cast)
        except ValueError:
            raise RuntimeError(f"Não foi possível converter '{value_to_cast}' para o tipo {target_type}.")

        raise RuntimeError(f"Conversão de tipo desconhecida: {target_type}.")

    # --- OPERATION NODES (that calculate values) ---

    def visit_BinOpNode(self, node):  # (ATUALIZADO)
        """ Executes binary operations (e.g., 1 ➕ 2, x ⚖️ 10, a 🤝 b). """
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
                raise RuntimeError("Divisão por zero.")
            return left_val / right_val

        # Comparison Operations
        elif op_type == TT_COMP_EQ:
            return left_val == right_val
        elif op_type == TT_COMP_GT:
            return left_val > right_val
        elif op_type == TT_COMP_LT:
            return left_val < right_val

        # (NOVO) Logic Operations
        elif op_type == TT_LOGIC_AND:
            return bool(left_val) and bool(right_val)
        elif op_type == TT_LOGIC_OR:
            return bool(left_val) or bool(right_val)

        raise RuntimeError(f"Operador binário desconhecido: {op_type}")

    def visit_UnaryOpNode(self, node):
        """ Executes unary operations (e.g., 🚫 x). """
        op_type = node.op_token.type
        value = self.visit(node.node)

        if op_type == TT_LOGIC_NOT:
            return not bool(value)  # Cast para booleano para segurança

        raise RuntimeError(f"Operador unário desconhecido: {op_type}")

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
            raise RuntimeError(f"Variável '{var_name}' já foi declarada.")

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
            raise RuntimeError(f"Variável '{var_name}' não declarada. Use 🔢, 💬, etc. para declarar.")

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
            raise RuntimeError(f"Variável '{var_name}' não declarada. Não é possível ler.")

        # Get the *current* type of the variable to try converting the input
        current_value = self.symbol_table[var_name]
        input_str = input(f"Insira o valor para {var_name}: ")

        try:
            if isinstance(current_value, int):
                new_value = int(input_str)
            elif isinstance(current_value, float):
                new_value = float(input_str)
            else:
                # If it's String, List, etc., just save the string
                new_value = input_str
        except ValueError:
            raise RuntimeError(f"Entrada inválida. Esperado um tipo compatível com '{var_name}'.")

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

    def visit_WhileNode(self, node):  # (NOVO)
        """ ⏳ (Loop "While") - Executa um bloco enquanto a condição for verdadeira. """
        while self.visit(node.condition_node):
            self.visit(node.body_node)

    def visit_ForNode(self, node):  # (NOVO)
        """ 🚶 (Loop "For Each") - Executa um bloco para cada item em uma lista. """
        list_val = self.visit(node.list_node)
        var_name = node.var_name_token.value

        if not isinstance(list_val, list):
            raise RuntimeError(f"Não é possível iterar 🚶 em algo que não é uma lista 📜.")

        # Gerenciamento de escopo: Salva o valor antigo da variável de iteração (se existir)
        old_value = self.symbol_table.get(var_name, None)

        for item in list_val:
            self.symbol_table[var_name] = item
            self.visit(node.body_node)

        # Restaura o valor antigo (ou remove se não existia)
        if old_value is not None:
            self.symbol_table[var_name] = old_value
        elif var_name in self.symbol_table:
            # Se não tinha valor antigo, remove a variável do escopo
            del self.symbol_table[var_name]

    # --- FUNCTION COMMANDS (ATUALIZADO) ---

    def visit_FuncDefNode(self, node):
        """ 🧩 (Definir Função) - Armazena a definição da função na memória. """
        func_name = node.func_name
        if func_name in self.symbol_table:
            raise RuntimeError(f"Função ou variável '{func_name}' já foi definida.")

        # A "função" é o próprio nó AST.
        self.symbol_table[func_name] = node

    def visit_FuncCallNode(self, node):  # (NOVO)
        """ 📞 (Chamar Função) - Executa uma função definida. """
        func_name = node.node_to_call.var_name
        func_def_node = self.symbol_table.get(func_name)

        if func_def_node is None:
            raise RuntimeError(f"Função '{func_name}' não foi definida 🧩.")
        if not isinstance(func_def_node, FuncDefNode):
            raise RuntimeError(f"'{func_name}' não é uma função 🧩. Não é possível chamar 📞.")

        # 1. Checar número de argumentos
        expected_count = len(func_def_node.arg_name_tokens)
        given_count = len(node.arg_nodes)
        if expected_count != given_count:
            raise RuntimeError(f"Função '{func_name}' espera {expected_count} argumentos, mas recebeu {given_count}.")

        # 2. Avaliar os argumentos (no escopo ATUAL)
        arg_values = [self.visit(arg_node) for arg_node in node.arg_nodes]

        # 3. Gerenciamento de escopo: Salvar variáveis
        arg_names = [token.value for token in func_def_node.arg_name_tokens]
        saved_vars = {}
        for name in arg_names:
            if name in self.symbol_table:
                saved_vars[name] = self.symbol_table[name]

        # 4. Injetar argumentos no escopo
        for name, value in zip(arg_names, arg_values):
            self.symbol_table[name] = value

        # 5. Executar o corpo da função (e capturar o 'return')
        return_value = None  # Funções retornam 'None' (nulo) por padrão
        try:
            self.visit(func_def_node.body_node)
        except ReturnSignal as rs:
            return_value = rs.value

        # 6. Limpar o escopo (restaurar variáveis antigas)
        for name in arg_names:
            if name in saved_vars:
                self.symbol_table[name] = saved_vars[name]
            else:
                # Se não existia antes, remova
                del self.symbol_table[name]

        return return_value

    def visit_ReturnNode(self, node):  # (ATUALIZADO)
        """ 🔙 (Return) - Envia o sinal de retorno para parar a execução da função. """
        value_to_return = None
        if node.node_to_return:
            value_to_return = self.visit(node.node_to_return)

        raise ReturnSignal(value_to_return)

    # --- LIST COMMANDS ---

    def visit_ListAppendNode(self, node):
        list_name = node.list_var_token.value
        list_obj = self.symbol_table.get(list_name)

        if list_obj is None:
            raise RuntimeError(f"Variável de lista '{list_name}' não encontrada.")
        if not isinstance(list_obj, list):
            raise RuntimeError(f"'{list_name}' não é uma lista 📜. Não é possível usar ➕📜.")

        value_to_append = self.visit(node.value_node)
        list_obj.append(value_to_append)

    def visit_ListRemoveNode(self, node):
        list_name = node.list_var_token.value
        list_obj = self.symbol_table.get(list_name)

        if not isinstance(list_obj, list):
            raise RuntimeError(f"'{list_name}' não é uma lista 📜. Não é possível usar ➖📜.")

        index_to_remove = self.visit(node.index_node)
        if not isinstance(index_to_remove, int):
            raise RuntimeError("Índice para remoção (➖📜) deve ser um inteiro 🔢.")

        try:
            list_obj.pop(index_to_remove)
        except IndexError:
            raise RuntimeError(f"Índice {index_to_remove} fora do alcance para a lista '{list_name}'.")

    # --- SYSTEM COMMANDS ---

    def visit_SaveNode(self, node):
        """ 💾 <data> <filename> 🔚 """
        data = self.visit(node.data_node)
        filename = self.visit(node.filename_node)

        if not isinstance(filename, str):
            raise RuntimeError("Nome do arquivo para 💾 (Salvar) deve ser uma string 💬.")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(data))
        except Exception as e:
            raise RuntimeError(f"Falha ao salvar o arquivo: {e}")

    def visit_FileAppendNode(self, node):  # (NOVO)
        """ ✍️ (Anexar Arquivo) <data> <filename> 🔚 """
        data = self.visit(node.data_node)
        filename = self.visit(node.filename_node)

        if not isinstance(filename, str):
            raise RuntimeError("Nome do arquivo para ✍️ (Anexar) deve ser uma string 💬.")

        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(str(data))
        except Exception as e:
            raise RuntimeError(f"Falha ao anexar ao arquivo: {e}")

    def visit_SleepNode(self, node):
        """ ⏱️ <duration> 🔚 """
        duration = self.visit(node.duration_node)

        try:
            time.sleep(float(duration))
        except (ValueError, TypeError):
            raise RuntimeError("Duração para ⏱️ (Sleep) deve ser um número (int ou real).")

    def visit_ImportNode(self, node):  # (ATUALIZADO)
        """ ⚙️ (Importar) <module_name> 🔚 """

        # Importações locais para evitar dependência circular
        from .lexer import Lexer
        from .parser import Parser, SyntaxError

        module_name = node.module_name_token.value
        filename = f"{module_name}.moji"

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo de módulo '{filename}' não encontrado para importar ⚙️.")
        except Exception as e:
            raise RuntimeError(f"Erro ao ler módulo '{filename}': {e}")

        # Executar o pipeline completo no código importado
        try:
            lexer = Lexer(code)
            tokens = lexer.make_tokens()
            parser = Parser(tokens)
            ast = parser.parse()

            # Executa o código importado em um *novo* interpretador
            # para que ele tenha seu próprio escopo
            import_interpreter = Interpreter()
            import_interpreter.run(ast)

            # Mescla os símbolos (funções, variáveis) do módulo no escopo atual
            for key, value in import_interpreter.symbol_table.items():
                if key in self.symbol_table:
                    # Evita sobrescrever variáveis existentes
                    raise RuntimeError(f"Importação ⚙️ de '{filename}' falhou: '{key}' já existe no escopo atual.")
                self.symbol_table[key] = value

        except (SyntaxError, RuntimeError) as e:
            raise RuntimeError(f"Erro ao importar ⚙️ o módulo '{filename}':\n{e}")


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