# This module contains the implementation of the cipher "Hill cipher"
import math

import numpy as np
from sympy.ntheory.primetest import is_square
from sympy import Matrix

from ..utils import get_letters_alphabetically
from ..common import EncProc


class HillError(Exception):
    """The exception that is thrown when an error occurs in the Hill class"""
    pass


class Hill:
    def __init__(self, key: str, alphabet: str) -> None:
        """
        Hill class constructor.

        Args:
            key: a string consisting of alphabetic characters. If the condition is not met,
                an HillError exception will be thrown.

            alphabet: a string consisting of various characters. The number of characters
                in a string should preferably be a prime number, otherwise it may be necessary
                to select a different size.
        """
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

        # Checking the conditions of the algorithm.
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
        """
        Data encryption/decryption method.

        Args:
            text: the string to be encrypted or decrypted.
            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise HillError("Input text is empty!")

        match enc_proc:
            case EncProc.ENCRYPT:
                matrix_key = self.matrix_key

            case EncProc.DECRYPT:
                # We are looking for the inverse matrix modulo and use it as a key.
                matrix_key = np.array(Matrix(self.matrix_key).inv_mod(len(self.alphabet)))

            case _:
                raise HillError(f"Invalid processing type! -> {enc_proc}")

        # We take only those letters that satisfy the alphabet.
        letters, indices = get_letters_alphabetically(text, self.alphabet)

        n = math.isqrt(len(self.key))

        new_letters = ""
        for i in range(0, len(letters), n):
            # We form a vector of indices and pad with zeros if there are not enough characters.
            vct = list(map(lambda x: self.alphabet.index(x.lower()), letters[i:i + n]))
            vct += [0 for _ in range(len(vct), n)]

            # We multiply the key matrix by the vector and translate the indices into symbols.
            new_vct = np.matmul(matrix_key, vct) % len(self.alphabet)
            new_letters += "".join(map(lambda x: self.alphabet[x], new_vct))

        # We place the encrypted letters in the places from which they were taken.
        text_list = list(text + new_letters[len(letters)::])
        for i, index in enumerate(indices):
            old_letter = text_list[index]
            new_letter = new_letters[i]

            if old_letter.isupper():
                new_letter = new_letter.upper()

            text_list[index] = new_letter

        return "".join(text_list)

    def encrypt(self, text: str) -> str:
        """
        Method - interface for encrypting input data.

        Args:
            text: the string to be encrypted.

        Returns:
            Encrypted string.
        """
        return self._transform(text, EncProc.ENCRYPT)

    def decrypt(self, text: str) -> str:
        """
        Method - interface for decrypting input data.

        Args:
            text: the string to be decrypted.

        Returns:
            Decrypted string.
        """
        return self._transform(text, EncProc.DECRYPT)

    def make(self, text: str, enc_proc: EncProc.ENCRYPT = EncProc.ENCRYPT) -> str:
        """
        Method - interface for encrypting/decrypting input data.

        Args:
            text: the string to be encrypted or decrypted.

            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).
                If the data object is of a different type, then an exception will be raised HillError.

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
