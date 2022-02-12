from random import choice
from copy import deepcopy

import numpy as np


class Field:
    def __init__(self, value: int, cond: bool = False):
        self.value = value
        self.cond = cond

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"Field({self.value}, {self.cond})"

    def __eq__(self, other):
        return self.value * self.cond == other


def check_correct_stencil(square: np.array) -> bool:
    s_1 = square
    s_2 = np.rot90(s_1, -1)
    s_3 = np.rot90(s_2, -1)
    s_4 = np.rot90(s_3, -1)

    n, _ = square.shape

    # If nothing is selected
    if len(np.where(s_1 != 0)[0]) < 1:
        return False

    # Check for matching values
    for i in range(n):
        for j in range(n):
            if [s_1[i, j].cond, s_2[i, j].cond, s_3[i, j].cond, s_4[i, j].cond].count(True) > 1:
                return False

    return True


def gen_stencil(k: int):
    if k < 2:
        raise Exception(f"K (k={k}) must be greater than 1!")

    square_1 = [list(Field(j) for j in range(i*k + 1, i*k + k + 1)) for i in range(k)]
    square_2 = deepcopy(square_1)
    square_3 = deepcopy(square_1)
    square_4 = deepcopy(square_1)

    squares = (square_1, square_2, square_3, square_4)

    for i in range(k):
        for j in range(k):
            square = choice(squares)
            square[i][j].cond = True

    square_2 = np.rot90(square_2, -1)
    square_3 = np.rot90(square_3, -2)
    square_4 = np.rot90(square_4, -3)

    rect_1 = np.concatenate((square_1, square_2), axis=1)
    rect_2 = np.concatenate((square_4, square_3), axis=1)

    square = np.concatenate((rect_1, rect_2), axis=0)

    return square


def encrypt(
        _text: str,
        stencil: np.ndarray,
        litter_type: str = "without_trash"
) -> str:
    n, _ = stencil.shape

    indices_allow_values = np.where(stencil != 0)
    sorted_allow_values = sorted(stencil[indices_allow_values], key=lambda x: x.value)

    one_iter_len_text = len(sorted_allow_values) * 4

    texts = [_text[i:i + one_iter_len_text] for i in range(0, len(_text), one_iter_len_text)]

    encrypted_text = ""

    for text in texts:
        square = np.empty((n, n), dtype=str)
        square.fill("")

        for i in range(0, len(text), len(sorted_allow_values)):
            substr = text[i:i+len(sorted_allow_values)]

            for char, value in zip(substr, sorted_allow_values):
                indices_value = np.where(stencil == value)
                square[indices_value] = char

            stencil = np.rot90(stencil, -1)

        indices = np.where(square == "")
        match litter_type:
            case "With trash":
                rand_letters = [choice(_text) for _ in range(len(indices[0]))]
                square[indices] = rand_letters

            case "Without trash":
                square[indices] = " "

            case _:
                raise Exception("Invalid trash type!")

        encrypted_text += "".join("".join(i) for i in square)

    return encrypted_text.rstrip()


def decrypt(
        _text: str,
        stencil: np.ndarray
):
    n, _ = stencil.shape

    indices_allow_values = np.where(stencil != 0)
    sorted_allow_values = sorted(stencil[indices_allow_values], key=lambda x: x.value)

    encrypted_texts = [_text[i:i + n**2] for i in range(0, len(_text), n**2)]
    encrypted_texts[-1] += " " * (n**2 - len(encrypted_texts[-1]))

    decrypted_text = ""

    for text in encrypted_texts:
        square = np.array(list(text)).reshape((n, n))

        for _ in range(4):
            for value in sorted_allow_values:
                i, j = np.where(stencil == value)
                decrypted_text += str(square[i[0], j[0]])

            stencil = np.rot90(stencil, -1)

    return decrypted_text.rstrip()


def make(
        text: str,
        stencil: np.ndarray,
        litter_type: str = "without_trash",
        processing_type: str = "Encrypt"
):
    match processing_type:
        case "Encrypt":
            return encrypt(text, stencil, litter_type)

        case "Decrypt":
            return decrypt(text, stencil)

        case _:
            raise Exception("Invalid processing type!")
