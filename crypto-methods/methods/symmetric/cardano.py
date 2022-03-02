from random import choice
from copy import deepcopy

import numpy as np


class CarganGrilleError(Exception):
    pass


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
    """Stencil validation function.

    Args:
        square: any square stencil.

    Returns:
        True - if the stencil is correct, otherwise False
    """
    s_1 = square
    s_2 = np.rot90(s_1, -1)
    s_3 = np.rot90(s_2, -1)
    s_4 = np.rot90(s_3, -1)

    n, m = square.shape
    if n != m or n < 2 or m < 2:
        return False

    # If nothing is selected
    if len(np.where(s_1 != 0)[0]) < 1:
        return False

    # Check for matching values
    for i in range(n):
        for j in range(n):
            if [s_1[i, j].cond, s_2[i, j].cond, s_3[i, j].cond, s_4[i, j].cond].count(True) > 1:
                return False

    return True


def gen_stencil(k: int) -> np.ndarray:
    """Random stencil generation function.

    Args:
        k: size of the side of the small square.

    Returns:
        Randomly generated stencil (numpy array).
    """
    if k < 2:
        raise CarganGrilleError("Error K value must be greater than 1!")

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

    square = np.concatenate((rect_1, rect_2), axis=0, dtype=Field)
    return square


def encrypt(
        text: str,
        stencil: np.ndarray,
        litter_type: str = "without trash"
) -> str:
    """Cardan grille cipher. Encryption function.

    Args:
        text: text to be encrypted.
        stencil: numpy array with elements of type Field.
        litter_type: encryption with or without garbage (default "without trash").

    Returns:
        Encrypted string.
    """
    if not text:
        raise CarganGrilleError("Input text is empty!")

    if not check_correct_stencil(stencil):
        raise CarganGrilleError("Wrong stencil!")

    n, _ = stencil.shape

    # We are looking for all the cells in the stencil where there are holes
    # Next, we take all these cells and sort them by values
    indices_allow_values = np.where(stencil != 0)
    sorted_allow_values = sorted(stencil[indices_allow_values], key=lambda x: x.value)

    one_iter_len_text = len(sorted_allow_values) * 4

    text_blocks = [text[i:i + one_iter_len_text] for i in range(0, len(text), one_iter_len_text)]

    encrypted_text = ""

    for text_block in text_blocks:
        square = np.empty((n, n), dtype=str)
        square.fill("")

        for i in range(0, len(text_block), len(sorted_allow_values)):
            substr = text_block[i:i+len(sorted_allow_values)]

            for char, value in zip(substr, sorted_allow_values):
                indices_value = np.where(stencil == value)
                square[indices_value] = char

            stencil = np.rot90(stencil, -1)

        indices = np.where(square == "")
        match litter_type:
            case "with trash":
                rand_letters = [choice(text) for _ in range(len(indices[0]))]
                square[indices] = rand_letters

            case "without trash":
                square[indices] = " "

            case _:
                raise CarganGrilleError("Invalid trash type!")

        encrypted_text += "".join("".join(i) for i in square)

    return encrypted_text


def decrypt(
        text: str,
        stencil: np.ndarray
) -> str:
    """Cardan grille cipher. Decryption function.

    Args:
        text: text to be decrypted.
        stencil: numpy array with elements of type Field.

    Returns:
        Decrypted string.
    """
    if not text:
        raise CarganGrilleError("Input text is empty!")

    if not check_correct_stencil(stencil):
        raise CarganGrilleError("Wrong stencil!")

    n, _ = stencil.shape

    indices_allow_values = np.where(stencil != 0)
    sorted_allow_values = sorted(stencil[indices_allow_values], key=lambda x: x.value)

    text_blocks = [text[i:i + n ** 2] for i in range(0, len(text), n ** 2)]
    text_blocks[-1] += " " * (n**2 - len(text_blocks[-1]))

    decrypted_text = ""

    for text_block in text_blocks:
        square = np.array(list(text_block)).reshape((n, n))

        for _ in range(4):
            for value in sorted_allow_values:
                i, j = np.where(stencil == value)
                decrypted_text += str(square[i[0], j[0]])

            stencil = np.rot90(stencil, -1)

    return decrypted_text


def make(
        text: str,
        stencil: np.ndarray,
        litter_type: str = "without trash",
        mode: str = "encrypt"
) -> str:
    """Cardan grille cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        stencil: numpy array with elements of type Field.
        litter_type: encryption with or without garbage (default "without trash").
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    match mode:
        case "encrypt":
            return encrypt(text, stencil, litter_type)

        case "decrypt":
            return decrypt(text, stencil)

        case _:
            raise CarganGrilleError(f"Invalid processing type! -> {mode}")
