<p align="center">
    <img src="/resources/icons/icon-app-128px.png" alt="preview">
</p>
<div>
    <h1 align="center">Crypto-methods</h1>
    <h2 align="center">Encrypt | Decrypt</h2>
    <p align="center">Laboratory work on cryptographic methods of information protection</p>
</div>

![crypto-methods-image1](/resources/screenshots/image1.png)


# :gear: Dependencies
<br>
> Python version must be 3.10+

- `python`
- `PyQt6`
- `numpy`
- `sympy`
- `PyYAML`

<br>

## Installation

We clone the repository and go to the project:

```zsh
git clone https://github.com/vasilypht/Cryptographic-methods
cd Cryptographic-methods
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

## Usage

To run the program, go to the source folder and run the file ***app.py***:

```zsh
cd crypto-methods
python3 app.py
```

