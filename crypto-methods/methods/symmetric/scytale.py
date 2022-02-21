
class ScytaleError(Exception):
    pass


def encrypt(text: str, n: int, m: int, auto_m: bool = True) -> str:
    """
     Scytale cipher. Encryption function.

     Parameters:
         text (str): text to be encrypted.
         n (int): number of rows.
         m (int): number of columns.
         auto_m (bool): calculate number of columns automatically (default True).

     Returns:
         text (str): encrypted text.
     """
    if not text:
        raise ScytaleError("Input text is empty!")

    if n <= 0 or m <= 0:
        raise ScytaleError("'n' and 'm' must be positive!")

    if auto_m:
        m = (len(text) - 1) // n + 1

    lines_list: list[list[str]] = []

    for i in range(n):
        line = list(text[i * m:(i + 1) * m])
        line += (m - len(line)) * [" "]
        lines_list.append(line)

    flip_lines_list = [i for i in zip(*lines_list)]
    return "".join("".join(i) for i in flip_lines_list)


def decrypt(text: str, n: int) -> str:
    """
    Scytale cipher. Decryption function.

    Parameters:
        text (str): text to be decrypted.
        n (int): number of rows.

    Returns:
        text (str): decrypted text.
    """
    if not text:
        raise ScytaleError("Input text is empty!")

    if n <= 0:
        raise ScytaleError("'n' must be positive!")

    lines_list: list[str] = []

    for i in range(n):
        line = text[i:len(text):n]
        lines_list.append(line)

    return "".join(lines_list)


def make(
        text: str,
        n: int,
        m: int,
        auto_m: bool = True,
        mode: str = "encrypt",
) -> str:
    """
    Scytale cipher. Interface for calling encryption/decryption functions.

    Parameters:
        text (str): text to be encrypted/decrypted.
        n (int): number of rows.
        m (int): number of columns.
        auto_m (bool): calculate number of columns automatically (default True).
        mode (str): encryption or decryption (default "encrypt").

    Returns:
        text (str): encrypted/decrypted text.
    """
    match mode:
        case "encrypt":
            return encrypt(text, n, m, auto_m)

        case "decrypt":
            return decrypt(text, n)

        case _:
            raise ScytaleError(f"Invalid processing type! -> {mode}")
