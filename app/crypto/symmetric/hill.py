import math

import numpy as np
from sympy.ntheory.primetest import (
    is_square
)
from sympy import (
    Matrix
)

from ..utils import (
    get_letters_alphabetically
)


class HillError(Exception):
    pass


def transform(
        text: str,
        key: str,
        alphabet: str,
        mode: str = "encrypt"
) -> str:
    """Hill Cipher. Encryption/decryption function.

    Args:
        text: text to be encrypted/decrypted.
        key: a set of letters of the same alphabet.
        alphabet: alphabet compiled by the user.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise HillError("Input text is empty!")

    if not key:
        raise HillError("The key is missing!")

    if not alphabet:
        raise HillError("Alphabet is empty!")

    if not is_square(len(key)):
        raise HillError("Key length must be a square!")

    if not set(key.lower()).issubset(alphabet):
        raise HillError("The key must be alphabetic characters!")

    if len(alphabet) != len(set(alphabet)):
        raise HillError("The alphabet must be composed of unique characters!")

    n = math.isqrt(len(key))
    matrix_key = np.array(list(map(lambda x: alphabet.index(x.lower()), key))).reshape((n, n))

    matrix_key_det = int(np.linalg.det(matrix_key))
    if matrix_key_det == 0:
        raise HillError("Matrix determinant is zero! The matrix is degenerate!")

    if math.gcd(matrix_key_det, len(alphabet)) != 1:
        raise HillError("Matrix determinant and key length must be coprime!")

    match mode:
        case "encrypt":
            pass

        case "decrypt":
            matrix_key = np.array(Matrix(matrix_key).inv_mod(len(alphabet)))

        case _:
            raise HillError(f"Invalid processing type! -> {mode}")

    letters, indices = get_letters_alphabetically(text, alphabet)

    new_letters = ""
    for i in range(0, len(letters), n):
        vct = list(map(lambda x: alphabet.index(x.lower()), letters[i:i + n]))
        vct += [0 for _ in range(len(vct), n)]

        new_vct = np.matmul(matrix_key, vct) % len(alphabet)
        new_letters += "".join(map(lambda x: alphabet[x], new_vct))

    text_list = list(text + new_letters[len(letters)::])
    for i, index in enumerate(indices):
        old_letter = text_list[index]
        new_letter = new_letters[i]

        if old_letter.isupper():
            new_letter = new_letter.upper()

        text_list[index] = new_letter

    return "".join(text_list)


def encrypt(
        text: str,
        key: str,
        alphabet: str
):
    """Hill Cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        key: a set of letters of the same alphabet.
        alphabet: alphabet compiled by the user.

    Returns:
        Encrypted string.
    """
    return transform(text, key, alphabet, "encrypt")


def decrypt(
        text: str,
        key: str,
        alphabet: str
):
    """Hill Cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        key: a set of letters of the same alphabet.
        alphabet: alphabet compiled by the user.

    Returns:
        Decrypted string.
    """
    return transform(text, key, alphabet, "decrypt")


def make(
        text: str,
        key: str,
        alphabet: str,
        mode: str = "encrypt"
):
    """Hill Cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        key: a set of letters of the same alphabet.
        alphabet: alphabet compiled by the user.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    match mode:
        case "encrypt":
            return encrypt(text, key, alphabet)

        case "decrypt":
            return decrypt(text, key, alphabet)

        case _:
            raise HillError(f"Invalid processing type! -> {mode}")
