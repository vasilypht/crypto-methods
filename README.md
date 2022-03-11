<p align="center">
    <img src="/resources/crypto-methods.png" alt="preview" height="128" width="128">
</p>
<div>
    <h1 align="center">Crypto-methods</h1>
    <h2 align="center">Encrypt | Decrypt</h2>
    <p align="center">Laboratory work on cryptographic methods of information protection</p>
</div>

![image-app](/resources/screenshots/image-app.png)

![image-vernam](/resources/screenshots/image-vernam.png)


# :books: Contents

- [**Supported ciphers**](#fire-supported-ciphers)
- [**Dependencies**](#gear-dependencies)
- [**Installation**](#hammer_and_wrench-installation)
- [**Usage**](#usage)
- [**Attribution links**](#link-attribution-links)

<br>

# :fire: Supported ciphers


| Method    | Module                                                            | Description                                                           |
|-----------|-------------------------------------------------------------------|-----------------------------------------------------------------------|
| Symmetric | [`atbash.py`](/src/crypto/symmetric/atbash.py)        | [Atbash cipher](https://en.wikipedia.org/wiki/Atbash)                 |
|           | [`scytale.py`](/src/crypto/symmetric/scytale.py)      | [Scytale cipher](https://en.wikipedia.org/wiki/Scytale)               |
|           | [`polybius.py`](/src/crypto/symmetric/polybius.py)    | [Polybius square](https://en.wikipedia.org/wiki/Polybius_square)      |
|           | [`caesar.py`](/src/crypto/symmetric/caesar.py)        | [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher)          |
|           | [`cardano.py`](/src/crypto/symmetric/cardano.py)      | [Cardan grille](https://en.wikipedia.org/wiki/Cardan_grille)          |
|           | [`richelieu.py`](/src/crypto/symmetric/richelieu.py)  | Richelieu cipher                                                      |
|           | [`alberti.py`](/src/crypto/symmetric/alberti.py)      | [Alberti cipher](https://en.wikipedia.org/wiki/Alberti_cipher)        |
|           | [`gronsfeld.py`](/src/crypto/symmetric/gronsfeld.py)  | Gronsfeld cipher                                                      |
|           | [`vigenere.py`](/src/crypto/symmetric/vigenere.py)    | [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher) |
|           | [`playfair.py`](/src/crypto/symmetric/playfair.py)    | [Playfair cipher](https://en.wikipedia.org/wiki/Playfair_cipher)      |
|           | [`hill.py`](/src/crypto/symmetric/hill.py)            | [Hill cipher](https://en.wikipedia.org/wiki/Hill_cipher)              |
|           | [`vernam.py`](/src/crypto/symmetric/vernam.py)        | [Vernam cipher](https://en.wikipedia.org/wiki/One-time_pad)           |

<br>

# :gear: Dependencies

- `python-3.10+`
- `PyQt6`
- `numpy`
- `sympy`
- `PyYAML`

<br>

# :hammer_and_wrench: Installation

We clone the repository and go to the project:

```zsh
git clone https://github.com/vasilypht/Cryptographic-methods
cd Cryptographic-crypto
```

Next, you need to install the dependencies. This can be done in one of the following ways:

 1. for **poetry**:
    
    Create a shell:
 
    ```zsh
    poetry shell
    ```
    
    Next, install all dependencies:

    ```zsh
    poetry install --no-dev
    ```

 2. for **virtualenv**:

    Creating a virtual environment and activate it:

    ```zsh
    python3 -m venv .venv
    . ./.venv/bin/activate
    ```
    
    Next, update pip and install all dependencies:

    ```zsh
    pip install -U pip
    pip install -r requirements.txt
    ```

<br>

## Usage

To run the program, go to the source folder and run the file ***app.py***:

```zsh
cd src
python3 app.py
```

# :link: Attribution links

- <a href="https://www.flaticon.com/free-icons/cyber-security" title="cyber security icons">Cyber security icons created by Graphix's Art - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/telegram" title="telegram icons">Telegram icons created by Freepik - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/vk" title="VK icons">VK icons created by Fathema Khanom - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/github" title="github icons">Github icons created by Pixel perfect - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/paper" title="paper icons">Paper icons created by inipagistudio - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/files-and-folders" title="files and folders icons">Files and folders icons created by inipagistudio - Flaticon</a>
