import re


class RichelieuError(Exception):
    pass


def transform(
        text: str,
        key: str,
        mode: str = "encrypt"
) -> str:
    """Richelieu cipher. Encryption/decryption function.

    Args:
        text: text to be encrypted/decrypted.
        key: format string (1,3,2)(1,2)...
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise RichelieuError("Input text is empty!")

    if not key:
        raise RichelieuError("The key is missing!")

    if not re.match(r"^\(\d+(,\d+|\)\(\d+)*\)$", key):
        raise RichelieuError("Invalid key entered!")

    # parse key str
    key_list = key.strip("()").split(")(")
    for i in range(len(key_list)):
        subkey = key_list[i].split(",")
        key_list[i] = list(map(int, subkey))

    # check range
    for subkey in key_list:
        for i in range(1, len(subkey) + 1):
            if i not in subkey:
                raise RichelieuError("Invalid key entered!")

    text_list: list[str] = list(text)

    text_index = 0
    key_index = 0

    while True:
        subkey = key_list[key_index]

        if text_index + len(subkey) > len(text):
            break

        substr = text[text_index:text_index + len(subkey)]

        for i, k in enumerate(subkey):
            match mode:
                case "encrypt":
                    text_list[text_index + k - 1] = substr[i]

                case "decrypt":
                    text_list[text_index + i] = substr[k - 1]

                case _:
                    raise RichelieuError(f"Invalid processing type! -> {mode}")

        text_index += len(subkey)
        key_index = (key_index + 1) % len(key_list)

    return "".join(text_list)


def encrypt(text: str, key: str) -> str:
    """Richelieu cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        key: format string (1,3,2)(1,2)...

    Returns:
        Encrypted string.
    """
    return transform(text, key, "encrypt")


def decrypt(text: str, key: str) -> str:
    """Richelieu cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        key: format string (1,3,2)(1,2)...

    Returns:
        Decrypted string.
    """
    return transform(text, key, "decrypt")


def make(
        text: str,
        key: str,
        mode: str = "encrypt"
) -> str:
    """Richelieu cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        key: format string (1,3,2)(1,2)...
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    match mode:
        case "encrypt":
            return encrypt(text, key)

        case "decrypt":
            return decrypt(text, key)

        case _:
            raise RichelieuError(f"Invalid processing type! -> {mode}")
