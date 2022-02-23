import re

from ..utils import (
    get_alphabet_by_letter
)


class GronsfeldError(Exception):
    pass


def transform(text: str, key: str, mode: str = "encrypt") -> str:
    """Gronsfeld cipher. Encryption/Decryption function.

    Args:
        text: text to be encrypted/decrypted.
        key: set of positive numbers.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise GronsfeldError("Input text is empty!")

    if not key:
        raise GronsfeldError("The key is missing!")

    if not re.match(r"^\d*$", key):
        raise GronsfeldError("Invalid key!")

    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_text = text_list[i]

        if (alphabet_lang := get_alphabet_by_letter(letter_text)) is None:
            continue

        alphabet_letter, _ = alphabet_lang
        letter_text_index = alphabet_letter.index(letter_text.lower())
        shift = int(key[i % len(key)])

        # choice of sign
        match mode:
            case "encrypt":
                sign = 1

            case "decrypt":
                sign = -1

            case _:
                raise GronsfeldError(f"Invalid processing type! -> {mode}")

        new_letter_index = (letter_text_index + shift * sign) % len(alphabet_letter)
        new_letter_text = alphabet_letter[new_letter_index]

        if letter_text.isupper():
            new_letter_text = new_letter_text.upper()

        text_list[i] = new_letter_text

    return "".join(text_list)


def encrypt(text: str, key: str) -> str:
    """Gronsfeld cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        key: set of positive numbers.

    Returns:
        Encrypted string.
    """
    return transform(text, key, "encrypt")


def decrypt(text: str, key: str) -> str:
    """Gronsfeld cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        key: set of positive numbers.

    Returns:
        Decrypted string.
    """
    return transform(text, key, "decrypt")


def make(
        text: str,
        key: str,
        mode: str = "encrypt"
):
    """Gronsfeld cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        key: set of positive numbers.
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
            raise GronsfeldError(f"Invalid processing type! -> {mode}")
