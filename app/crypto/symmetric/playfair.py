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


class PlayfairError(Exception):
    pass


class Playfair:
    def __init__(self, key: str):
        if not key:
            raise PlayfairError("The key is missing!")

        if not re.match(r"(^[а-яА-ЯёЁ]*$)|(^[a-zA-Z]*$)", key):
            raise PlayfairError("Invalid key!")

        self.key = key

    def _transform(self, text: str, enc_proc: EncProc) -> str:
        """Playfair cipher. Encryption/Decryption function.

        Args:
            text: text to be encrypted/decrypted.
            enc_proc: encryption or decryption (default "encrypt").

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

        match lang:
            case Languages.ENGLISH:
                shape = (5, 5)
                letter_swap = ("j", "i")
                first_add_letter = "x"
                second_add_letter = "y"

            case Languages.RUSSIAN:
                shape = (4, 8)
                letter_swap = ("ъ", "ь")
                first_add_letter = "х"
                second_add_letter = "у"

            case _:
                raise NotImplementedError()

        alphabet = alphabet.replace(letter_swap[0], "")
        text = text.replace(*letter_swap)

        key = self.key.lower()
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

    def encrypt(self, text: str) -> str:
        """Playfair cipher. Interface for calling encryption functions.

        Args:
            text: text to be encrypted.

        Returns:
            Encrypted string.
        """
        return self._transform(text, EncProc.ENCRYPT)

    def decrypt(self, text: str) -> str:
        """Playfair cipher. Interface for calling decryption functions.

        Args:
            text: text to be decrypted.

        Returns:
            Decrypted string.
        """
        return self._transform(text, EncProc.DECRYPT)

    def make(self, text: str, enc_proc: EncProc = EncProc.ENCRYPT) -> str:
        """Playfair cipher. Interface for calling encryption/decryption functions.

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
                raise PlayfairError(f"Invalid processing type! -> {enc_proc}")
