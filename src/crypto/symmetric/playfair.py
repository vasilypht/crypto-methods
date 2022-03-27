import re

import numpy as np

from ..utils import (
    get_alphabet_by_letter,
    get_letters_alphabetically
)
from ..const import (
    ALPHABETS
)


class PlayfairError(Exception):
    pass


def transform(text: str, key: str, mode: str = "encrypt") -> str:
    """Playfair cipher. Encryption/Decryption function.

    Args:
        text: text to be encrypted/decrypted.
        key: a set of letters of the same alphabet.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise PlayfairError("Input text is empty!")

    if not key:
        raise PlayfairError("The key is missing!")

    if not re.match(r"(^[а-яА-ЯёЁ]*$)|(^[a-zA-Z]*$)", key):
        raise PlayfairError("Invalid key!")

    match mode:
        case "encrypt":
            key_sign = 1

        case "decrypt":
            key_sign = -1

        case _:
            raise PlayfairError(f"Invalid processing type! -> {mode}")

    alphabet, lang = get_alphabet_by_letter(key[0], ALPHABETS)

    match lang:
        case "en":
            shape = (5, 5)
            letter_swap = ("j", "i")
            first_add_letter = "x"
            second_add_letter = "y"

        case "ru":
            shape = (4, 8)
            letter_swap = ("ъ", "ь")
            first_add_letter = "х"
            second_add_letter = "у"

        case _:
            raise Exception("Error lang!")

    alphabet = alphabet.replace(letter_swap[0], "")
    text = text.replace(*letter_swap)

    key = key.lower()
    key = key.replace(*letter_swap)

    # added key + alphabet
    unique_letters = []
    for letter in key + alphabet:
        if letter not in unique_letters:
            unique_letters.append(letter)

    key_matrix = np.array(unique_letters).reshape(shape)

    # split to bigrams
    letters, indices = get_letters_alphabetically(text, alphabet)
    bigrams = [letters[i:i + 2] for i in range(0, len(letters), 2)]

    if not bigrams:
        return text

    if len(bigrams[-1]) == 1:
        bigrams[-1] += first_add_letter

    transformed_letters = ""
    for first_letter, second_letter in bigrams:
        # first rule
        if first_letter == second_letter:
            # If the letters are equal to the additional letter,
            # then it is necessary to replace the second one with a new additional letter
            if first_letter == first_add_letter:
                second_letter = second_add_letter
            else:
                second_letter = first_add_letter

        # get indices
        first_letter_i, first_letter_j = np.where(key_matrix == first_letter.lower())
        second_letter_i, second_letter_j = np.where(key_matrix == second_letter.lower())

        if first_letter_i[0] == second_letter_i[0]:
            first_letter_j[0] = (first_letter_j[0] + 1 * key_sign) % shape[1]
            second_letter_j[0] = (second_letter_j[0] + 1 * key_sign) % shape[1]

        elif first_letter_j[0] == second_letter_j[0]:
            first_letter_i[0] = (first_letter_i + 1 * key_sign) % shape[0]
            second_letter_i[0] = (second_letter_i + 1 * key_sign) % shape[0]

        else:
            first_letter_j, second_letter_j = second_letter_j, first_letter_j

        new_firs_letter = key_matrix[first_letter_i, first_letter_j][0]
        new_second_letter = key_matrix[second_letter_i, second_letter_j][0]

        transformed_letters += new_firs_letter.upper() if first_letter.isupper() else new_firs_letter
        transformed_letters += new_second_letter.upper() if second_letter.isupper() else new_second_letter

    text_list: list[str] = list(text + transformed_letters[len(indices)::])

    for i, letter_index in enumerate(indices):
        text_list[letter_index] = transformed_letters[i]

    return "".join(text_list)


def encrypt(text: str, key: str) -> str:
    """Playfair cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        key: a set of letters of the same alphabet.

    Returns:
        Encrypted string.
    """
    return transform(text, key, "encrypt")


def decrypt(text: str, key: str) -> str:
    """Playfair cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        key: a set of letters of the same alphabet.

    Returns:
        Decrypted string.
    """
    return transform(text, key, "decrypt")


def make(text: str, key: str, mode: str = "encrypt") -> str:
    """Playfair cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        key: a set of letters of the same alphabet.
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
            raise PlayfairError(f"Invalid processing type! -> {mode}")
