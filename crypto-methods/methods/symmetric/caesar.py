from ..utils import (
    get_alphabet_by_letter
)


def transform(text: str, shift: int = 1, mode: bool = True) -> str:
    """
    Caesar's cipher. Encryption/decryption function.

    Parameters:
        text (str): text to be encrypted.
        shift (int): alphabet shift (default 1).
        mode (bool): True - encrypt, False - decrypt (default True).

    Returns:
        text (str): encrypted text.
    """
    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_text = text_list[i]
        if (alphabet_lang := get_alphabet_by_letter(letter_text)) is None:
            continue

        alphabet_letter_text, _ = alphabet_lang
        letter_text_index = alphabet_letter_text.index(letter_text.lower())

        # choice of sign
        sign = 1 if mode else -1

        new_letter_text_index = (letter_text_index + shift * sign) % len(alphabet_letter_text)
        new_letter_text = alphabet_letter_text[new_letter_text_index]

        if letter_text.isupper():
            new_letter_text = new_letter_text.upper()

        text_list[i] = new_letter_text

    return "".join(text_list)


def encrypt(text: str, shift: int = 1) -> str:
    """
    Caesar's cipher. Encryption function.

    Parameters:
        text (str): text to be encrypted.
        shift (int): alphabet shift (default 1).

    Returns:
        text (str): encrypted text.
    """
    return transform(text, shift, True)


def decrypt(text: str, shift: int = 1) -> str:
    """
    Caesar's cipher. Decryption function.

    Parameters:
        text (str): text to be decrypted.
        shift (int): alphabet shift (default 1).

    Returns:
        text (str): decrypted text.
    """
    return transform(text, shift, False)


def make(text: str, shift: int = 1, processing_type: str = "encrypt") -> str:
    """
    Caesar's cipher. Interface for calling encryption/decryption functions.

    Parameters:
        text (str): text to be encrypted/decrypted.
        shift (int): alphabet shift (default 1).
        processing_type (str): encryption or decryption (default "encrypt").

    Returns:
        text (str): encrypted/decrypted text.
    """
    match processing_type:
        case "encrypt":
            return encrypt(text, shift)

        case "decrypt":
            return decrypt(text, shift)

        case _:
            raise Exception("Invalid processing type!")
