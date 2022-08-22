# This module contains the implementation of the cipher "Playfair cipher"
import re

import numpy as np

from ..utils import (
    get_alphabet_by_letter,
    get_letters_alphabetically
)
from ..const import ALPHABET_TABLE
from ..common import (
    EncProc,
    Languages
)
from ..exceptions import PlayfairError


class Playfair:
    def __init__(self, key: str) -> None:
        """
        Playfair class constructor.

        Args:
            key: a string consisting only of the Russian or only of the English alphabet.
        """
        if not key:
            raise PlayfairError("The key is missing!")

        if not re.match(r"(^[а-яё]*$)|(^[a-z]*$)", key, re.IGNORECASE):
            raise PlayfairError("Invalid key!")

        self.key = key

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
            raise PlayfairError("Input text is empty!")

        match enc_proc:
            case EncProc.ENCRYPT:
                key_sign = 1

            case EncProc.DECRYPT:
                key_sign = -1

            case _:
                raise PlayfairError(f"Invalid processing type! -> {enc_proc}")

        lang, alphabet = get_alphabet_by_letter(self.key[0], ALPHABET_TABLE)

        # We initialize the substitution rules for alphabets.
        match lang:
            case Languages.ENGLISH:
                shape = (5, 5)
                # Which letter to change and to what.
                letter_swap = ("j", "i")

                # We initialize the letters to which the same letters in bigrams will change.
                first_add_letter = "x"
                second_add_letter = "y"

            case Languages.RUSSIAN:
                shape = (4, 8)
                # Which letter to change and to what.
                letter_swap = ("ъ", "ь")

                # We initialize the letters to which the same letters in bigrams will change.
                first_add_letter = "х"
                second_add_letter = "у"

            case _:
                raise NotImplementedError()

        # We remove from the alphabet a letter that we will not process.
        alphabet = alphabet.replace(letter_swap[0], "")
        # We replace the letters according to the rule.
        text = text.replace(*letter_swap)

        key = self.key.lower()
        key = key.replace(*letter_swap)

        # We get unique characters from the alphabet and the key, preserving the order.
        unique_letters = []
        for letter in key + alphabet:
            if letter not in unique_letters:
                unique_letters.append(letter)

        key_matrix = np.array(unique_letters).reshape(shape)

        # We take only those letters that satisfy the alphabet.
        letters, indices = get_letters_alphabetically(text, alphabet)
        bigrams = [letters[i:i + 2] for i in range(0, len(letters), 2)]

        if not bigrams:
            return text

        if len(bigrams[-1]) == 1:
            bigrams[-1] += first_add_letter

        transformed_letters = ""
        for first_letter, second_letter in bigrams:
            if first_letter == second_letter:
                # If the letters are equal to the additional letter,
                # then it is necessary to replace the second one with a new additional letter
                if first_letter == first_add_letter:
                    second_letter = second_add_letter
                else:
                    second_letter = first_add_letter

            # We get the indices of letters from the matrix.
            first_letter_i, first_letter_j = np.where(key_matrix == first_letter.lower())
            second_letter_i, second_letter_j = np.where(key_matrix == second_letter.lower())

            # Based on the rules, we form new indices.
            if first_letter_i[0] == second_letter_i[0]:
                first_letter_j[0] = (first_letter_j[0] + 1 * key_sign) % shape[1]
                second_letter_j[0] = (second_letter_j[0] + 1 * key_sign) % shape[1]

            elif first_letter_j[0] == second_letter_j[0]:
                first_letter_i[0] = (first_letter_i + 1 * key_sign) % shape[0]
                second_letter_i[0] = (second_letter_i + 1 * key_sign) % shape[0]

            else:
                first_letter_j, second_letter_j = second_letter_j, first_letter_j

            # Getting new letters.
            new_firs_letter = key_matrix[first_letter_i, first_letter_j][0]
            new_second_letter = key_matrix[second_letter_i, second_letter_j][0]

            # Adding new letters to the rest, respecting the case of old letters.
            transformed_letters += new_firs_letter.upper() if first_letter.isupper() else new_firs_letter
            transformed_letters += new_second_letter.upper() if second_letter.isupper() else new_second_letter

        text_list: list[str] = list(text + transformed_letters[len(indices)::])

        for i, letter_index in enumerate(indices):
            text_list[letter_index] = transformed_letters[i]

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

    def make(self, text: str, enc_proc: EncProc = EncProc.ENCRYPT) -> str:
        """
        Method - interface for encrypting/decrypting input data.

        Args:
            text: the string to be encrypted or decrypted.

            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).
                If the data object is of a different type, then an exception will be raised PlayfairError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise PlayfairError(f"Invalid processing type! -> {enc_proc}")
