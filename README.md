# Moji 🐻 
### An Emoji-Powered Programming Language

[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg?style=for-the-badge&logo=googletranslate&logoColor=white)](https://github.com/ArtFaz/Moji/blob/main/README_PTBR.md)
[![en](https://img.shields.io/badge/lang-en-red.svg?style=for-the-badge&logo=googletranslate&logoColor=white)](https://github.com/ArtFaz/Moji/blob/main/README.md)

[![Status](https://img.shields.io/badge/status-stable-green.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ArtFaz/Moji)
[![Latest Release](https://img.shields.io/github/v/release/ArtFaz/Moji?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ArtFaz/moji/releases/latest)
[![Language](https://img.shields.io/badge/language-Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) 
[![License](https://img.shields.io/badge/license-MIT-gold.svg?style=for-the-badge)](LICENSE)

Moji is a fully functional interpreter for a programming language that uses emojis as its core syntax. Instead of `if`, `else`, or `print`, Moji uses `🤔`, `🤨`, and `🖨️`. 

This project was created as the final assignment for the Compiler course at Unisagrado.


## ✨ Features

* **Expressive Syntax:** Write code using intuitive emojis.
* **Core Logic:** Full support for variables, conditional logic (`if/elif/else`), and loops (`while`/`for`).
* **Data Types:** Handles Integers (`🔢`), Reals/Floats (`👽`), Strings (`💬`), and Lists (`📜`).
* **I/O:** Print (`🖨️`), Read Input (`👀`), and File Operations (`💾`/`📖`/`✍️`).
* **Functions:** Define and call reusable code blocks (`🧩`/`📞`).
* **Math & Logic:** Arithmetic (`➕`, `➖`...) and Boolean Logic (`🤝`, `🌀`, `🚫`).
* **Built in Python:** Uses pure python 🐍 for every step involved.

## 👋 Hello, Moji!

Here’s a simple "Hello, World!" program in Moji that also shows variable math:

```
🌱
💭 This is a "Hello World!" and math test.

💬 hello 👉 "Hello" 🔚
💬 world 👉 "Moji!" 🔚
🖨️ hello ➕ " " ➕ world 🔚 💭 String concatenation

🔢 a 👉 10 🔚
👽 b 👉 5.5 🔚
👽 sum 👉 a ➕ b 🔚

🖨️ "Sum (10 + 5.5): " ➕ sum 🔚
🌳
```

## 📖 The Great Moji-pedia (Language Reference)

Below is the official dictionary for the Moji language.

| Category | Emoji | Meaning | Description |
|-----------|--------|----------|-------------|
| **Program Structure** | 🌱 | Start Program | Begins the program |
| | 🌳 | End Program | Ends the program |
| **Code Blocks** | 📦 | Start of Code Block | Opens a code block |
| | 📦⛔ | End of Code Block | Closes a code block |
| **Variables** | 🔢 | Integer | Declares an integer variable or casts to int |
| | 👽 | Real | Declares a real (float) variable or casts to float |
| | 💬 | String | Declares a string variable or casts to string |
| | 📜 | List | Creates a list |
| **Input / Output** | 👀 | Read | Reads input into a variable |
| | 🖨️ | Print | Prints variable content |
| **Math Operations** | ➕ | Add | Addition |
| | ➖ | Subtract | Subtraction |
| | ✖️ | Multiply | Multiplication |
| | ➗ | Divide | Division |
| **Assignment** | 👉 | Assign | Assigns a value to a variable |
| **Comments & Syntax** | 💭 | Comment | Marks a comment line |
| | 🔚 | End Command | End of a statement |
| **Conditionals** | 🤔 | If | Executes if condition is true |
| | 🔀 | Elif | Executes if another condition is true |
| | 🤨 | Else | Executes if all conditions are false |
| **Loops** | ⏳ | While | Loop while condition is true |
| | 🚶 | For Each | Iterates through items in a list |
| **Functions** | 🧩 | Define Function | Defines a new function |
| | 📞 | Call Function | Calls/Executes a defined function |
| | 🔙 | Return | Returns a value from a function |
| **Logic & Comparison** | ⚖️ | Equals | Compares equality |
| | ⬆️ | Greater Than | Checks if greater |
| | ⬇️ | Less Than | Checks if smaller |
| | 🚫 | Not | Logical negation |
| | 🤝 | And | Logical AND |
| | 🌀 | Or | Logical OR |
| **Lists** | ➕📜 | Append | Adds item to a list |
| | ➖📜 | Remove | Removes item from a list |
| | 🎯 | Get At | Access item at specific index |
| **System & Misc.** | 💾 | Save | Saves data to a file (overwrite) |
| | ✍️ | Append File | Appends data to a file |
| | 📖 | Read File | Reads content from a file |
| | ⚙️ | Import | Imports another .moji file |
| | ⏱️ | Sleep | Waits or delays execution |

## 🏃‍♂️ How to Run Moji

We offer two easy ways to run your Moji code.

### ⭐️ Method 1: Run in your Browser (Google Colab)

No installation required! We have prepared a Google Colab notebook that lets you write and run Moji code directly in your browser. This is the fastest and easiest way to try Moji.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArtFaz/Moji/blob/main/PlaygroundMoji.ipynb)

### 💻 Method 2: Run Locally (CLI)

You can run Moji on your local machine by following these steps:

**Clone the repository:**

```bash
git clone https://github.com/ArtFaz/Moji
cd moji
```

**Create and activate a virtual environment (recommended):**

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies:** All dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

**Run a Moji file:** To run a Moji program (we use the `.moji` file extension), pass the file path to our main interpreter script:

```bash
python main.py examples/condicionais.moji
```

Check the `/examples` folder for more sample code!


## 🛠️ Built with ❤️ by the Moji Team

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
This project is licensed under the MIT License - see the `LICENSE` file for details.
