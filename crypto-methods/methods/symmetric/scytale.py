
class ScytaleError(Exception):
    pass


def encrypt(text: str, n: int, m: int, auto_m: bool = True) -> str:
    """Scytale cipher. Encryption function.

    Args:
        text: text to be encrypted.
        n: number of rows.
        m: number of columns.
        auto_m: calculate number of columns automatically (default True).

    Returns:
        Encrypted string.
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
    """Scytale cipher. Decryption function.

    Args:
        text: text to be decrypted.
        n: number of rows.

    Returns:
        Decrypted string.
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
    """Scytale cipher. Interface for calling encryption/decryption functions.

    Args:
        text: ext to be encrypted/decrypted.
        n: number of rows.
        m: number of columns.
        auto_m: calculate number of columns automatically (default True).
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    match mode:
        case "encrypt":
            return encrypt(text, n, m, auto_m)

        case "decrypt":
            return decrypt(text, n)

        case _:
            raise ScytaleError(f"Invalid processing type! -> {mode}")
