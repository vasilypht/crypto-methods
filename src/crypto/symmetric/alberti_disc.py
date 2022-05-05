import re

from ..utils import (
    get_alphabet_by_letter
)
from ..const import (
    ALPHABET_TABLE
)


class AlbertiError(Exception):
    pass


def transform(
        text: str,
        key: str,
        step: int = 0,
        shift: int = 0,
        mode: str = "encrypt"
) -> str:
    """Alberti disc cipher. Encryption/decryption function.

    Args:
        text: text to be encrypted/decrypted.
        key: a set of letters of the same alphabet.
        step: offset after each iteration.
        shift: offset from the beginning of the internal alphabet.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise AlbertiError("Input text is empty!")

    if not key:
        raise AlbertiError("The key is missing!")

    if not re.match(r"(^[а-яё]*$)|(^[a-z]*$)", key, re.IGNORECASE):
        raise AlbertiError("Invalid key!")

    _, external_alphabet = get_alphabet_by_letter(key[0], ALPHABET_TABLE)

    internal_alphabet = ""
    for letter in key.lower() + external_alphabet:
        if letter not in internal_alphabet:
            internal_alphabet += letter

    # Making a shift in the internal alphabet
    internal_alphabet = internal_alphabet[shift::] + internal_alphabet[:shift:]

    match mode:
        case "encrypt":
            key_sign = 1

        case "decrypt":
            # swap alphabets
            internal_alphabet, external_alphabet = external_alphabet, internal_alphabet
            key_sign = -1

        case _:
            raise AlbertiError(f"Invalid processing type! -> {mode}")

    text_list: list[str] = list(text)
    internal_shift = 0

    for i in range(len(text)):
        letter = text_list[i]

        if (letter_pos := external_alphabet.find(letter.lower())) == -1:
            continue

        new_letter_pos = (letter_pos + internal_shift) % len(internal_alphabet)
        new_letter = internal_alphabet[new_letter_pos]

        internal_shift = (internal_shift + step * key_sign) % len(internal_alphabet)

        if letter.isupper():
            new_letter = new_letter.upper()

        text_list[i] = new_letter

    return "".join(text_list)


def encrypt(
        text: str,
        key: str,
        step: int = 0,
        shift: int = 0
) -> str:
    """Alberti disc cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        key: a set of letters of the same alphabet.
        step: offset after each iteration.
        shift: offset from the beginning of the internal alphabet.

    Returns:
        Encrypted string.
    """
    return transform(text, key, step, shift, "encrypt")


def decrypt(
        text: str,
        key: str,
        step: int = 0,
        shift: int = 0
) -> str:
    """Alberti disc cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        key: a set of letters of the same alphabet.
        step: offset after each iteration.
        shift: offset from the beginning of the internal alphabet.

    Returns:
        Decrypted string.
    """
    return transform(text, key, step, shift, "decrypt")


def make(
        text: str,
        key: str,
        step: int = 0,
        shift: int = 0,
        mode: str = "encrypt"
) -> str:
    """Alberti disc cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        key: a set of letters of the same alphabet.
        step: offset after each iteration.
        shift: offset from the beginning of the internal alphabet.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    match mode:
        case "encrypt":
            return encrypt(text, key, step, shift)

        case "decrypt":
            return decrypt(text, key, step, shift)

        case _:
            raise AlbertiError(f"Invalid processing type! -> {mode}")
