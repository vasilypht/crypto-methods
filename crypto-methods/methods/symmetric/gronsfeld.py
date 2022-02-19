from ..const import (
    RUS_LCASE,
    ENG_LCASE
)


def encrypt(text: str, key: str) -> str:
    """
    Gronsfeld cipher. Encryption function.

    Parameters:
        text (str): text to be encrypted.
        key (str): set of positive numbers.

    Returns:
        text (str): encrypted text.
    """
    text_list = list(text)

    for i in range(len(text)):
        letter_lower = text_list[i].lower()

        for alpha in (ENG_LCASE, RUS_LCASE):
            if letter_lower not in alpha:
                continue

            letter_index = alpha.index(letter_lower)
            shift = int(key[i % len(key)])

            new_index = (letter_index + shift) % len(alpha)
            new_letter = alpha[new_index]

            if text_list[i].isupper():
                new_letter = new_letter.upper()

            text_list[i] = new_letter
            break

    return "".join(text_list)


def decrypt(text: str, key: str) -> str:
    """
    Gronsfeld cipher. Decryption function.

    Parameters:
        text (str): text to be decrypted.
        key (str): set of positive numbers.

    Returns:
        text (str): decrypted text.
    """
    text_list = list(text)

    for i in range(len(text)):
        letter_lower = text_list[i].lower()

        for alpha in (ENG_LCASE, RUS_LCASE):
            if letter_lower not in alpha:
                continue

            letter_index = alpha.index(letter_lower)
            shift = int(key[i % len(key)])

            new_index = (letter_index - shift) % len(alpha)
            new_letter = alpha[new_index]

            if text_list[i].isupper():
                new_letter = new_letter.upper()

            text_list[i] = new_letter
            break

    return "".join(text_list)


def make(
        text: str,
        key: str,
        processing_type: str = "encrypt"
):
    """
    Gronsfeld cipher. Interface for calling encryption/decryption functions.

    Parameters:
        text (str): text to be encrypted/decrypted.
        key (str): set of positive numbers.
        processing_type (str): encryption or decryption (default "encrypt").

    Returns:
        text (str): encrypted/decrypted text.
    """
    match processing_type:
        case "encrypt":
            return encrypt(text, key)

        case "decrypt":
            return decrypt(text, key)

        case _:
            raise Exception("Invalid processing type!")
