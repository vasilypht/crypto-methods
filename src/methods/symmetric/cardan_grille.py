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
    one_iter_len = (n//2) ** 2
    max_len = n**2

    texts = [_text[i:i+max_len] for i in range(0, len(_text), max_len)]
    encrypted_text = ""

    for text in texts:
        square = np.empty((n, n), dtype=str)
        square.fill("")

        for i in range(0, len(text), one_iter_len):
            substr = text[i:i+one_iter_len]

            for k, char in enumerate(substr, start=1):
                i, j = np.where(stencil == k)
                square[i, j] = char

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

    return encrypted_text


def decrypt(
        _text: str,
        stencil: np.ndarray
):
    n, _ = stencil.shape
    one_iter_len = (n//2) ** 2
    max_len = n ** 2

    encrypted_texts = [_text[i:i + max_len] for i in range(0, len(_text), max_len)]
    encrypted_texts[-1] += " " * (max_len - len(encrypted_texts[-1]))

    decrypted_text = ""

    for text in encrypted_texts:
        square = np.array(list(text)).reshape((n, n))

        for _ in range(4):
            for k in range(1, one_iter_len + 1):
                i, j = np.where(stencil == k)
                decrypted_text += str(square[i[0], j[0]])

            stencil = np.rot90(stencil, -1)

    return decrypted_text


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
