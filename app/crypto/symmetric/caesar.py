from ..utils import (
    get_alphabet_by_letter
)
from ..const import (
    ALPHABET_TABLE
)


class CaesarError(Exception):
    pass


def transform(text: str, shift: int = 1, mode: str = "encrypt") -> str:
    """Caesar's cipher. Encryption/decryption function.

    Args:
        text: text to be encrypted/decrypted.
        shift: alphabet shift (default 1).
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise CaesarError("Input text is empty!")

    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_text = text_list[i]
        if (lang_alphabet := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
            continue

        _, alphabet = lang_alphabet
        letter_text_index = alphabet.index(letter_text.lower())

        # choice of sign
        match mode:
            case "encrypt":
                sign = 1

            case "decrypt":
                sign = -1

            case _:
                raise CaesarError(f"Invalid processing type! -> {mode}")

        new_letter_text_index = (letter_text_index + shift * sign) % len(alphabet)
        new_letter_text = alphabet[new_letter_text_index]

        if letter_text.isupper():
            new_letter_text = new_letter_text.upper()

        text_list[i] = new_letter_text

    return "".join(text_list)


def encrypt(text: str, shift: int = 1) -> str:
    """Caesar cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        shift: alphabet shift (default 1).

    Returns:
        Encrypted string.
    """
    return transform(text, shift, "encrypt")


def decrypt(text: str, shift: int = 1) -> str:
    """Caesar cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        shift: alphabet shift (default 1).

    Returns:
        Decrypted string.
    """
    return transform(text, shift, "decrypt")


def make(text: str, shift: int = 1, mode: str = "encrypt") -> str:
    """Caesar cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        shift: alphabet shift (default 1).
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    match mode:
        case "encrypt":
            return encrypt(text, shift)

        case "decrypt":
            return decrypt(text, shift)

        case _:
            raise CaesarError(f"Invalid processing type! -> {mode}")
