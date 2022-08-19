import math

import numpy as np
from sympy.ntheory.primetest import is_square
from sympy import Matrix

from ..utils import get_letters_alphabetically
from ..common import EncProc


class HillError(Exception):
    pass


class Hill:
    def __init__(self, key: str, alphabet: str):
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

        self.matrix_key = matrix_key

        self.key = key
        self.alphabet = alphabet

    def _transform(self, text: str, enc_proc: EncProc) -> str:
        if not text:
            raise HillError("Input text is empty!")

        match enc_proc:
            case EncProc.ENCRYPT:
                matrix_key = self.matrix_key

            case EncProc.DECRYPT:
                matrix_key = np.array(Matrix(self.matrix_key).inv_mod(len(self.alphabet)))

            case _:
                raise HillError(f"Invalid processing type! -> {enc_proc}")

        letters, indices = get_letters_alphabetically(text, self.alphabet)

        n = math.isqrt(len(self.key))

        new_letters = ""
        for i in range(0, len(letters), n):
            vct = list(map(lambda x: self.alphabet.index(x.lower()), letters[i:i + n]))
            vct += [0 for _ in range(len(vct), n)]

            new_vct = np.matmul(matrix_key, vct) % len(self.alphabet)
            new_letters += "".join(map(lambda x: self.alphabet[x], new_vct))

        text_list = list(text + new_letters[len(letters)::])
        for i, index in enumerate(indices):
            old_letter = text_list[index]
            new_letter = new_letters[i]

            if old_letter.isupper():
                new_letter = new_letter.upper()

            text_list[index] = new_letter

        return "".join(text_list)

    def encrypt(self, text: str):
        """Hill Cipher. Interface for calling encryption functions.

        Args:
            text: text to be encrypted.

        Returns:
            Encrypted string.
        """
        return self._transform(text, EncProc.ENCRYPT)

    def decrypt(self, text: str):
        """Hill Cipher. Interface for calling decryption functions.

        Args:
            text: text to be decrypted.

        Returns:
            Decrypted string.
        """
        return self._transform(text, EncProc.DECRYPT)

    def make(self, text: str, enc_proc: EncProc.ENCRYPT):
        """Hill Cipher. Interface for calling encryption/decryption functions.

        Args:
            text: text to be encrypted/decrypted.
            enc_proc: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise HillError(f"Invalid processing type! -> {enc_proc}")
