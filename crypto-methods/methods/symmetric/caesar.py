from ..const import (
    RUS_LCASE,
    ENG_LCASE
)


def encrypt(text: str, shift: int = 1) -> str:
    """
    Caesar's cipher. Encryption function.

    Parameters:
        text (str): text to be encrypted.
        shift (int): alphabet shift (default 1).

    Returns:
        text (str): encrypted text.
    """
    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_lower = text_list[i].lower()

        for alphabet in (ENG_LCASE, RUS_LCASE):
            if letter_lower not in alphabet:
                continue

            pos = alphabet.index(letter_lower)
            new_pos = (pos + shift) % len(alphabet)

            new_letter = alphabet[new_pos]

            if text_list[i].isupper():
                new_letter = letter_lower.upper()

            text_list[i] = new_letter
            break

    return "".join(text_list)


def decrypt(text: str, shift: int = 1) -> str:
    """
    Caesar's cipher. Decryption function.

    Parameters:
        text (str): text to be decrypted.
        shift (int): alphabet shift (default 1).

    Returns:
        text (str): decrypted text.
    """
    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_lower = text_list[i].lower()

        for alphabet in (ENG_LCASE, RUS_LCASE):
            if letter_lower not in alphabet:
                continue

            pos = alphabet.index(letter_lower)
            new_pos = (pos - shift) % len(alphabet)

            new_letter = alphabet[new_pos]

            if text_list[i].isupper():
                new_letter = letter_lower.upper()

            text_list[i] = new_letter
            break

    return "".join(text_list)


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
