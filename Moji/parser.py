# moji/parser.py

# Importa todos os nós que o Parser pode construir
from .ast_nodes import (
    Node, ProgramNode, BlockNode, NumberNode, StringNode, VarAccessNode,
    BinOpNode, UnaryOpNode, VarDeclareNode, VarAssignNode, PrintNode,
    ReadNode, IfNode, FuncDefNode, ReturnNode, ListAppendNode,
    ListRemoveNode, ImportNode, SaveNode, SleepNode
)
# Importa todos os tipos de token que o Parser precisa reconhecer
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
# 1. ERRO DE SINTAXE
################################################################################

class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__(f"Erro de Sintaxe: {message}")


################################################################################
# 2. CLASSE PARSER
################################################################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        # Inicializa o token atual com o primeiro token da lista
        self.current_token = self.tokens[self.token_idx] if self.tokens else None

    def advance(self):
        """ Avança para o próximo token na lista. """
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            # Se não houver mais tokens, o token atual permanece o último (geralmente EOF)
            self.current_token = self.tokens[-1]
        return self.current_token

    def peek(self, n=1):
        """ Espia o token 'n' posições à frente sem avançar. """
        peek_idx = self.token_idx + n
        if peek_idx < len(self.tokens):
            return self.tokens[peek_idx]
        return None

    def eat(self, expected_token_type):
        """
        Consome o token atual se ele for do tipo esperado.
        Se não for, lança um erro de sintaxe.
        """
        if self.current_token.type == expected_token_type:
            self.advance()
        else:
            raise SyntaxError(
                f"Esperava '{expected_token_type}', mas encontrou '{self.current_token.type}'"
            )

    # --- PONTO DE PARTIDA (Nível mais alto) ---

    def parse(self):
        """
        Inicia a análise sintática.
        Um programa é: 🌱 ...lista de comandos... 🌳
        """
        self.eat(TT_PROGRAM_START)

        # statements() vai ler todos os comandos até encontrar o 🌳
        statements = self.statements(end_token_type=TT_PROGRAM_END)

        # Se statements() parou e não é o 🌳, algo está errado
        self.eat(TT_PROGRAM_END)

        # Se chegou aqui e o próximo token não é EOF, há código sobrando
        if self.current_token.type != TT_EOF:
            raise SyntaxError("Código encontrado após o fim do programa '🌳'.")

        return ProgramNode(statements)

    # --- COMANDOS (Statements) ---

    def statements(self, end_token_type):
        """
        Processa uma lista de comandos até encontrar um token final
        (ex: 🌳 para o programa, 📦⛔ para um bloco).
        """
        statement_list = []

        while self.current_token.type != end_token_type and self.current_token.type != TT_EOF:
            statement_list.append(self.statement())

        return statement_list

    def statement(self):
        """ Roteador: Decide qual tipo de comando está sendo lido. """
        token_type = self.current_token.type

        # 🖨️ ... 🔚 (Print)
        if token_type == TT_KEYWORD_PRINT:
            return self.print_statement()

        # 👀 ... 🔚 (Read)
        if token_type == TT_KEYWORD_READ:
            return self.read_statement()

        # 🔢, 💬, 👽, 📜 ... (Declaração de Var)
        if token_type in (TT_KEYWORD_INT, TT_KEYWORD_REAL, TT_KEYWORD_STRING, TT_KEYWORD_LIST):
            return self.var_declaration()

        # 🤔 ... (If)
        if token_type == TT_KEYWORD_IF:
            return self.if_statement()

        # 📦 ... 📦⛔ (Block)
        if token_type == TT_BLOCK_START:
            return self.block()

        # 🧩 ... (Definição de Função)
        if token_type == TT_KEYWORD_FUN:
            return self.func_definition()

        # 🔙 ... (Return)
        if token_type == TT_KEYWORD_RETURN:
            return self.return_statement()

        # ⚙️, 💾, ⏱️ (Comandos de Sistema)
        if token_type == TT_KEYWORD_IMPORT:
            return self.import_statement()
        if token_type == TT_KEYWORD_SAVE:
            return self.save_statement()
        if token_type == TT_KEYWORD_SLEEP:
            return self.sleep_statement()

        # Identificador (Pode ser Atribuição ou Op de Lista)
        if token_type == TT_IDENTIFIER:
            next_token_type = self.peek().type

            # x 👉 ... 🔚 (Atribuição)
            if next_token_type == TT_ASSIGN:
                return self.var_assignment()

            # myList ➕📜 ... 🔚 (List Append)
            if next_token_type == TT_KEYWORD_APPEND:
                return self.list_append()

            # myList ➖📜 ... 🔚 (List Remove)
            if next_token_type == TT_KEYWORD_REMOVE:
                return self.list_remove()

        # Se não for nada disso, é um erro.
        raise SyntaxError(f"Comando inesperado: token '{self.current_token}'")

    def print_statement(self):
        """ Processa: 🖨️ <expressão> 🔚 """
        self.eat(TT_KEYWORD_PRINT)
        node_to_print = self.expression()
        self.eat(TT_END_STATEMENT)
        return PrintNode(node_to_print)

    def read_statement(self):
        """ Processa: 👀 <identificador> 🔚 """
        self.eat(TT_KEYWORD_READ)
        var_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_END_STATEMENT)
        return ReadNode(var_token)

    def var_declaration(self):
        """ Processa: <tipo> <nome> [👉 <expressão>] 🔚 """
        type_token = self.current_token
        self.advance()  # Consome o tipo (🔢, 💬, etc.)

        var_name_token = self.current_token
        self.eat(TT_IDENTIFIER)

        value_node = None
        # Verifica se é uma declaração com inicialização
        if self.current_token.type == TT_ASSIGN:
            self.eat(TT_ASSIGN)
            value_node = self.expression()

        self.eat(TT_END_STATEMENT)
        return VarDeclareNode(type_token, var_name_token, value_node)

    def var_assignment(self):
        """ Processa: <nome> 👉 <expressão> 🔚 """
        var_name_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_ASSIGN)
        value_node = self.expression()
        self.eat(TT_END_STATEMENT)
        return VarAssignNode(var_name_token, value_node)

    def list_append(self):
        """ Processa: <nome_lista> ➕📜 <expressão> 🔚 """
        list_var_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_KEYWORD_APPEND)
        value_node = self.expression()
        self.eat(TT_END_STATEMENT)
        return ListAppendNode(list_var_token, value_node)

    def list_remove(self):
        """ Processa: <nome_lista> ➖📜 <expressão_indice> 🔚 """
        list_var_token = self.current_token
        self.eat(TT_IDENTIFIER)
        self.eat(TT_KEYWORD_REMOVE)
        index_node = self.expression()  # O índice a ser removido
        self.eat(TT_END_STATEMENT)
        return ListRemoveNode(list_var_token, index_node)

    def if_statement(self):
        """ Processa: 🤔 <cond> 📦 ... 📦⛔ [🔀 <cond> 📦 ... 📦⛔]* [🤨 📦 ... 📦⛔] """
        cases = []
        else_case = None

        # Bloco IF (obrigatório)
        self.eat(TT_KEYWORD_IF)
        condition = self.expression()
        body = self.block()
        cases.append((condition, body))

        # Blocos ELIF (opcionais)
        while self.current_token.type == TT_KEYWORD_ELIF:
            self.eat(TT_KEYWORD_ELIF)
            condition = self.expression()
            body = self.block()
            cases.append((condition, body))

        # Bloco ELSE (opcional)
        if self.current_token.type == TT_KEYWORD_ELSE:
            self.eat(TT_KEYWORD_ELSE)
            else_case = self.block()

        return IfNode(cases, else_case)

    def block(self):
        """ Processa: 📦 <lista_de_comandos> 📦⛔ """
        self.eat(TT_BLOCK_START)
        # statements() vai ler tudo até encontrar o 📦⛔
        statements_list = self.statements(end_token_type=TT_BLOCK_END)
        self.eat(TT_BLOCK_END)
        return BlockNode(statements_list)

    def func_definition(self):
        """ Processa: 🧩 <nome> [arg1] [arg2] ... 📦 ... 📦⛔ """
        self.eat(TT_KEYWORD_FUN)

        func_name_token = self.current_token
        self.eat(TT_IDENTIFIER)

        arg_name_tokens = []
        # Continua lendo nomes de argumentos até encontrar o 📦
        while self.current_token.type == TT_IDENTIFIER:
            arg_name_tokens.append(self.current_token)
            self.eat(TT_IDENTIFIER)

        body_node = self.block()
        return FuncDefNode(func_name_token, arg_name_tokens, body_node)

    def return_statement(self):
        """ Processa: 🔙 [<expressão>] 🔚 """
        self.eat(TT_KEYWORD_RETURN)

        node_to_return = None
        # Se houver algo para retornar (não é só "🔙 🔚")
        if self.current_token.type != TT_END_STATEMENT:
            node_to_return = self.expression()

        self.eat(TT_END_STATEMENT)
        return ReturnNode(node_to_return)

    # Comandos de sistema (simples)
    def import_statement(self):
        self.eat(TT_KEYWORD_IMPORT)
        module_name_token = self.current_token
        self.eat(TT_IDENTIFIER)  # Assumindo que importamos pelo nome
        self.eat(TT_END_STATEMENT)
        return ImportNode(module_name_token)

    def save_statement(self):
        self.eat(TT_KEYWORD_SAVE)
        data_node = self.expression()
        filename_node = self.expression()  # Ex: 💾 variavel "arquivo.txt" 🔚
        self.eat(TT_END_STATEMENT)
        return SaveNode(data_node, filename_node)

    def sleep_statement(self):
        self.eat(TT_KEYWORD_SLEEP)
        duration_node = self.expression()
        self.eat(TT_END_STATEMENT)
        return SleepNode(duration_node)

    # --- EXPRESSÕES (Precedência de Operadores) ---

    def binary_operation(self, func_to_call, valid_op_types):
        """
        Função auxiliar genérica para processar operações binárias
        (como 1 ➕ 2, ou 10 ⚖️ x)
        """
        left = func_to_call()

        while self.current_token.type in valid_op_types:
            op_token = self.current_token
            self.eat(op_token.type)
            right = func_to_call()
            left = BinOpNode(left, op_token, right)

        return left

    def expression(self):
        """ Ponto de entrada para qualquer expressão. (Nível mais baixo de precedência) """
        # Por enquanto, apenas comparações. Poderia expandir para 'E' e 'OU' lógicos.
        return self.comparison()

    def comparison(self):
        """ Processa: ⚖️, ⬆️, ⬇️ """
        return self.binary_operation(self.term, (TT_COMP_EQ, TT_COMP_GT, TT_COMP_LT))

    def term(self):
        """ Processa: ➕, ➖ """
        return self.binary_operation(self.factor, (TT_OP_PLUS, TT_OP_MINUS))

    def factor(self):
        """ Processa: ✖️, ➗ """
        return self.binary_operation(self.unary, (TT_OP_MUL, TT_OP_DIV))

    def unary(self):
        """ Processa: 🚫 """
        if self.current_token.type == TT_LOGIC_NOT:
            op_token = self.current_token
            self.eat(TT_LOGIC_NOT)
            node = self.unary()  # Chamada recursiva para permitir '🚫🚫x'
            return UnaryOpNode(op_token, node)
        return self.atom()

    def atom(self):
        """
        Processa os "átomos" da gramática: números, strings, nomes de vars.
        (Nível mais alto de precedência).
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
            return VarAccessNode(token)  # Acesso a uma variável

        # Se não for nada disso, é um erro de sintaxe na expressão
        raise SyntaxError(f"Esperava um Inteiro, Real, String ou Identificador, mas encontrou: {token}")


################################################################################
# 3. Bloco de Teste
# (Para executar este arquivo diretamente: python -m moji.parser)
################################################################################

if __name__ == '__main__':
    # Precisamos do Lexer para gerar os tokens primeiro
    from .lexer import Lexer

    # Código de exemplo do seu "hello_world.moji"
    test_code = """
    🌱 💭 Este é um programa de teste!

    💬 meuNome 👉 "Moji" 🔚
    🖨️ "Olá, " ➕ meuNome 🔚

    🔢 x 👉 10 🔚
    🤔 x ⚖️ 10 📦
        🖨️ "x é 10!" 🔚
    📦⛔

    🌳
    """

    print(f"--- Testando Parser com o código: ---\n{test_code}")

    try:
        # 1. Lexer
        lexer = Lexer(test_code)
        tokens = lexer.make_tokens()
        print("--- Tokens Gerados (pelo Lexer) ---")
        for t in tokens:
            print(t)

        # 2. Parser
        parser = Parser(tokens)
        ast = parser.parse()

        print("\n--- AST Gerada (pelo Parser) ---")
        print(ast)

    except Exception as e:
        print(f"\n!!! ERRO NO PARSER: {e}")