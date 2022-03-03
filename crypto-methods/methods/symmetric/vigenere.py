import re

from ..utils import (
    get_alphabet_by_letter
)
from ..const import (
    ALPHABETS
)


class VigenereError(Exception):
    pass


def transform(text: str, key: str, mode: str = "encrypt") -> str:
    """Vigenere cipher. Encryption/Decryption function.

    Args:
        text: text to be encrypted/decrypted.
        key: set of letters.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise VigenereError("Input text is empty!")

    if not key:
        raise VigenereError("The key is missing!")

    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]*$", key):
        raise VigenereError("Invalid key!")

    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_text = text_list[i]
        if (alphabet_lang_text := get_alphabet_by_letter(letter_text, ALPHABETS)) is None:
            continue

        letter_key = key[i % len(key)]
        if (alphabet_lang_key := get_alphabet_by_letter(letter_key, ALPHABETS)) is None:
            continue

        alphabet_letter_text, _ = alphabet_lang_text
        alphabet_letter_key, _ = alphabet_lang_key

        letter_text_index = alphabet_letter_text.index(letter_text.lower())
        letter_key_index = alphabet_letter_key.index(letter_key.lower())

        # choice of sign
        match mode:
            case "encrypt":
                key_sign = 1

            case "decrypt":
                key_sign = -1

            case _:
                raise VigenereError(f"Invalid processing type! -> {mode}")

        new_letter_text_index = (letter_text_index + letter_key_index * key_sign) % len(alphabet_letter_text)
        new_letter_text = alphabet_letter_text[new_letter_text_index]

        if letter_text.isupper():
            new_letter_text = new_letter_text.upper()

        text_list[i] = new_letter_text

    return "".join(text_list)


def encrypt(text: str, key: str) -> str:
    """Vigenere cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        key: set of letters.

    Returns:
        Encrypted string.
    """
    return transform(text, key, "encrypt")


def decrypt(text: str, key: str) -> str:
    """Vigenere cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        key: set of letters.

    Returns:
        Decrypted string.
    """
    return transform(text, key, "decrypt")


def make(text: str, key: str, mode: str) -> str:
    """Vigenere cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        key: set of letters.
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
            raise VigenereError(f"Invalid processing type! -> {mode}")
