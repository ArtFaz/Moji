# Moji 🐻 
### Uma Linguagem de Programação Baseada em Emojis

[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg?style=for-the-badge&logo=googletranslate&logoColor=white)](https://github.com/ArtFaz/Moji/blob/main/README_PTBR.md)
[![en](https://img.shields.io/badge/lang-en-red.svg?style=for-the-badge&logo=googletranslate&logoColor=white)](https://github.com/ArtFaz/Moji/blob/main/README.md)

[![Status](https://img.shields.io/badge/status-stable-green.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ArtFaz/Moji)
[![Latest Release](https://img.shields.io/github/v/release/ArtFaz/Moji?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ArtFaz/moji/releases/latest)
[![Language](https://img.shields.io/badge/language-Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) 
[![License](https://img.shields.io/badge/license-MIT-gold.svg?style=for-the-badge)](LICENSE)

O Moji é um interpretador totalmente funcional para uma linguagem de programação que usa emojis como sua sintaxe principal. Em vez de `if`, `else` ou `print`, o Moji usa `🤔`, `🤨` e `🖨️`.

Este projeto foi criado como trabalho final para a disciplina de Compiladores na Unisagrado.


## ✨ Funcionalidades

* **Sintaxe Expressiva:** Escreva código usando emojis intuitivos.
* **Lógica Central:** Suporte total a variáveis, lógica condicional (`if/elif/else`) e laços de repetição (`while`/`for`).
* **Tipos de Dados:** Suporta Inteiros (`🔢`), Reais/Floats (`👽`), Strings (`💬`) e Listas (`📜`).
* **Entrada / Saída:** Imprimir no console (`🖨️`), Ler entrada do usuário (`👀`) e Operações de Arquivo (`💾`/`📖`/`✍️`).
* **Funções:** Defina e chame blocos de código reutilizáveis (`🧩`/`📞`).
* **Matemática e Lógica:** Aritmética padrão (`➕`, `➖`...) e Lógica Booleana (`🤝`, `🌀`, `🚫`).
* **Feito em Python:** Utiliza Python puro 🐍 para cada etapa do processo.

## 👋 Olá, Moji!

Aqui está um programa simples "Olá, Mundo!" em Moji que também demonstra matemática com variáveis:

```
🌱
💭 Este é um teste de "Olá Mundo!" e matemática.

💬 ola 👉 "Olá" 🔚
💬 mundo 👉 "Moji!" 🔚
🖨️ ola ➕ " " ➕ mundo 🔚 💭 Concatenação de strings

🔢 a 👉 10 🔚
👽 b 👉 5.5 🔚
👽 soma 👉 a ➕ b 🔚

🖨️ "Soma de (10 + 5.5): " ➕ soma 🔚
🌳
```

## 📖 A Grande Moji-pédia (Referência da Linguagem)

Abaixo está o dicionário oficial da linguagem Moji.

| Categoria | Emoji | Significado | Descrição |
|-----------|--------|----------|-------------|
| **Estrutura do Programa** | 🌱 | Início do Programa | Inicia o programa |
| | 🌳 | Fim do Programa | Encerra o programa |
| **Blocos de Código** | 📦 | Início de Bloco | Abre um bloco de código |
| | 📦⛔ | Fim de Bloco | Fecha um bloco de código |
| **Variáveis** | 🔢 | Inteiro | Declara uma variável inteira ou converte para int |
| | 👽 | Real | Declara uma variável real (float) ou converte para float |
| | 💬 | String | Declara uma variável string ou converte para string |
| | 📜 | Lista | Cria uma lista |
| **Entrada / Saída** | 👀 | Ler | Lê a entrada do usuário para uma variável |
| | 🖨️ | Imprimir | Imprime o conteúdo de uma variável ou valor |
| **Operações Matemáticas** | ➕ | Adicionar | Adição |
| | ➖ | Subtrair | Subtração |
| | ✖️ | Multiplicar | Multiplicação |
| | ➗ | Dividir | Divisão |
| **Atribuição** | 👉 | Atribuir | Atribui um valor a uma variável |
| **Comentários e Sintaxe** | 💭 | Comentário | Marca uma linha de comentário |
| | 🔚 | Fim de Comando | Marca o final de uma instrução |
| **Condicionais** | 🤔 | Se (If) | Executa se a condição for verdadeira |
| | 🔀 | Senão Se (Elif) | Executa se outra condição for verdadeira |
| | 🤨 | Senão (Else) | Executa se todas as condições anteriores forem falsas |
| **Loops** | ⏳ | Enquanto (While) | Repete enquanto a condição for verdadeira |
| | 🚶 | Para Cada (For Each) | Itera através de itens em uma lista |
| **Funções** | 🧩 | Definir Função | Define uma nova função |
| | 📞 | Chamar Função | Chama/Executa uma função definida |
| | 🔙 | Retornar | Retorna um valor de uma função |
| **Lógica e Comparação** | ⚖️ | Igual | Compara igualdade |
| | ⬆️ | Maior Que | Verifica se é maior |
| | ⬇️ | Menor Que | Verifica se é menor |
| | 🚫 | Não (Not) | Negação lógica |
| | 🤝 | E (And) | E lógico |
| | 🌀 | Ou (Or) | Ou lógico |
| **Listas** | ➕📜 | Adicionar (Append) | Adiciona um item ao final da lista |
| | ➖📜 | Remover | Remove um item da lista pelo índice |
| | 🎯 | Pegar Em | Acessa um item em um índice específico |
| **Sistema e Diversos** | 💾 | Salvar | Salva dados em um arquivo (sobrescreve) |
| | ✍️ | Anexar Arquivo | Adiciona dados ao final de um arquivo |
| | 📖 | Ler Arquivo | Lê o conteúdo de um arquivo |
| | ⚙️ | Importar | Importa outro arquivo .moji |
| | ⏱️ | Dormir (Sleep) | Aguarda ou atrasa a execução |

## 🏃‍♂️ Como Executar o Moji

Oferecemos duas maneiras fáceis de executar seu código Moji.

### ⭐️ Método 1: Execute no seu Navegador (Google Colab)

Nenhuma instalação necessária! Preparamos um notebook do Google Colab que permite escrever e executar código Moji diretamente no seu navegador. Esta é a maneira mais rápida e fácil de testar o Moji.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArtFaz/Moji/blob/main/PlaygroundMoji.ipynb)

### 💻 Método 2: Executar Localmente (CLI)

Você pode executar o Moji na sua máquina local seguindo estes passos:

**Clone o repositório:**

```bash
git clone [https://github.com/ArtFaz/Moji](https://github.com/ArtFaz/Moji)
cd moji
```
**Crie e ative um ambiente virtual (recomendado):**

```bash
# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Instale as dependências:** Todas as dependências estão listadas no `requirements.txt`.

```bash
pip install -r requirements.txt
```

**Execute um arquivo Moji**: Para rodar um programa Moji (usamos a extensão de arquivo .moji), passe o caminho do arquivo para o nosso script interpretador principal:

```bash
python main.py examples/condicionais.moji
```

Confira a pasta `/examples` para mais códigos de exemplo!


## 🛠️ Feito com ❤️ pelo Time Moji

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/ArtFaz">
        <img src="https://avatars.githubusercontent.com/ArtFaz" width="80px" style="border-radius:50%;" alt="ArtFaz"/>
        <br />
        <sub><b>Arthur Fazioni</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/GabMartinezz">
        <img src="https://avatars.githubusercontent.com/GabMartinezz" width="80px" style="border-radius:50%;" alt="GabMartinezz"/>
        <br />
        <sub><b>Gabriel Martinez</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/LuisFelipeFilenga">
        <img src="https://avatars.githubusercontent.com/LuisFelipeFilenga" width="80px" style="border-radius:50%;" alt="Luis Felipe Filenga"/>
        <br />
        <sub><b>Luis Felipe Filenga</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/LeonardoCamposG">
        <img src="https://avatars.githubusercontent.com/LeonardoCamposG" width="80px" style="border-radius:50%;" alt="Leonardo Campos"/>
        <br />
        <sub><b>Leonardo Campos</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Matheus-Kaihara">
        <img src="https://avatars.githubusercontent.com/Matheus-Kaihara" width="80px" style="border-radius:50%;" alt="Matheus Kaihara"/>
        <br />
        <sub><b>Matheus Kaihara</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/MatheusGoes29">
        <img src="https://avatars.githubusercontent.com/MatheusGoes29" width="80px" style="border-radius:50%;" alt="Matheus Goes"/>
        <br />
        <sub><b>Matheus Goes</b></sub>
      </a>
    </td>
  </tr>
</table>



___
Este projeto está licenciado sob a Licença MIT - veja o arquivo `LICENSE` para detalhes.
