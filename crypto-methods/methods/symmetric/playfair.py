import numpy as np

from ..utils import (
    get_alphabet_by_letter
)


def split_into_bigrams(text: str, alphabet: str):
    indices = []
    letters = ""

    for i, letter in enumerate(text):
        if letter.lower() in alphabet:
            letters += letter
            indices.append(i)

    bigrams = [letters[i:i + 2] for i in range(0, len(letters), 2)]
    return bigrams, indices


def transform(text: str, key: str, mode: bool = True) -> str:
    sign = 1 if mode else -1
    alphabet, lang = get_alphabet_by_letter(key[0])

    match lang:
        case "en":
            shape = (5, 5)
            letter_swap = ("j", "i")
            additional_letter = "x"

        case "ru":
            shape = (4, 8)
            letter_swap = ("ъ", "ь")
            additional_letter = "х"

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

    bigrams, indices = split_into_bigrams(text, alphabet)
    if len(bigrams[-1]) == 1:
        bigrams[-1] += additional_letter

    transformed_letters = ""
    for first_letter, second_letter in bigrams:
        # first rule
        if first_letter == second_letter:
            second_letter = additional_letter

        # get indices
        first_letter_i, first_letter_j = np.where(key_matrix == first_letter.lower())
        second_letter_i, second_letter_j = np.where(key_matrix == second_letter.lower())

        if first_letter_i[0] == second_letter_i[0]:
            first_letter_j[0] = (first_letter_j[0] + 1 * sign) % shape[1]
            second_letter_j[0] = (second_letter_j[0] + 1 * sign) % shape[1]

        elif first_letter_j[0] == second_letter_j[0]:
            first_letter_i[0] = (first_letter_i + 1 * sign) % shape[0]
            second_letter_i[0] = (second_letter_i + 1 * sign) % shape[0]

        else:
            first_letter_j, second_letter_j = second_letter_j, first_letter_j

        new_firs_letter = key_matrix[first_letter_i, first_letter_j][0]
        new_second_letter = key_matrix[second_letter_i, second_letter_j][0]

        transformed_letters += new_firs_letter.upper() if first_letter.isupper() else new_firs_letter
        transformed_letters += new_second_letter.upper() if second_letter.isupper() else new_second_letter

    text_list: list[str] = list(text)

    for i, letter_index in enumerate(indices):
        text_list[letter_index] = transformed_letters[i]

    if len(indices) % 2 != 0:
        text_list.append(transformed_letters[-1])

    return "".join(text_list)


def encrypt(text: str, key: str) -> str:
    return transform(text, key, True)


def decrypt(text: str, key: str) -> str:
    return transform(text, key, False)


def make(text: str, key: str, mode: str) -> str:
    match mode:
        case "encrypt":
            return encrypt(text, key)

        case "decrypt":
            return decrypt(text, key)

        case _:
            raise Exception("Invalid processing type!")
