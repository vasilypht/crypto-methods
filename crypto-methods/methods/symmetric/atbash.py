from ..utils import (
    get_alphabet_by_letter
)


class AtbashError(Exception):
    pass


def transform(text: str) -> str:
    """
    Atbash cipher. Encryption/decryption function.

    Parameters:
        text (str): text to be encrypted/decrypted.

    Returns:
        text (str): encrypted/decrypted text.
    """

    if not text:
        raise AtbashError("Input text is empty!")

    letters_list: list[str] = list(text)

    for i in range(len(text)):
        letter_text = letters_list[i]

        if (alpha_lang := get_alphabet_by_letter(letter_text)) is None:
            continue

        alphabet, _ = alpha_lang
        letter_index = alphabet.index(letter_text.lower())
        new_letter = alphabet[len(alphabet) - letter_index - 1]

        if letter_text.isupper():
            new_letter = new_letter.upper()

        letters_list[i] = new_letter

    return "".join(letters_list)


def make(text: str) -> str:
    """
    Atbash cipher. Interface for calling encryption/decryption functions.

    Parameters:
        text (str): text to be encrypted/decrypted.

    Returns:
        text (str): encrypted/decrypted text.
    """
    return transform(text)
