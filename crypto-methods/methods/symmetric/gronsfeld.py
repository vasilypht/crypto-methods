from ..utils import (
    get_alphabet_by_letter
)


def transform(text: str, key: str, mode: bool = True) -> str:
    """
    Gronsfeld cipher. Encryption/Decryption function.

    Parameters:
        text (str): text to be encrypted.
        key (str): set of positive numbers.
        mode (bool): True - encrypt, False - decrypt

    Returns:
        text (str): encrypted text.
    """
    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_text = text_list[i]

        if (alphabet_lang := get_alphabet_by_letter(letter_text)) is None:
            continue

        alphabet_letter, _ = alphabet_lang
        letter_text_index = alphabet_letter.index(letter_text.lower())
        shift = int(key[i % len(key)])

        # choice of sign
        sign = 1 if mode else -1

        new_letter_index = (letter_text_index + shift * sign) % len(alphabet_letter)
        new_letter_text = alphabet_letter[new_letter_index]

        if letter_text.isupper():
            new_letter_text = new_letter_text.upper()

        text_list[i] = new_letter_text

    return "".join(text_list)


def encrypt(text: str, key: str) -> str:
    return transform(text, key, True)


def decrypt(text: str, key: str) -> str:
    return transform(text, key, False)


def make(
        text: str,
        key: str,
        mode: str = "encrypt"
):
    """
    Gronsfeld cipher. Interface for calling encryption/decryption functions.

    Parameters:
        text (str): text to be encrypted/decrypted.
        key (str): set of positive numbers.
        mode (str): encryption or decryption (default "encrypt").

    Returns:
        text (str): encrypted/decrypted text.
    """
    match mode:
        case "encrypt":
            return encrypt(text, key)

        case "decrypt":
            return decrypt(text, key)

        case _:
            raise Exception("Invalid processing type!")
