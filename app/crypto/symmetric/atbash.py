# This module contains the implementation of the cipher "Cipher Atbash"
from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE


class Atbash:
    def _transform(self, text: str) -> str:
        """
         Data encryption/decryption method.

        Args:
            text: the string to be encrypted or decrypted.

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise ""

        letters_list: list[str] = list(text)

        for i in range(len(text)):
            letter_text = letters_list[i]

            # For each letter of the text, we look for the corresponding alphabet.
            # If there is none, we skip the iteration, skipping the given letter.
            if (lang_alphabet := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
                continue

            _, alphabet = lang_alphabet

            # We get the index of the letter in the alphabet and
            # find a new one using the algorithm.
            letter_index = alphabet.index(letter_text.lower())
            new_letter = alphabet[len(alphabet) - letter_index - 1]

            if letter_text.isupper():
                new_letter = new_letter.upper()

            letters_list[i] = new_letter

        return "".join(letters_list)

    def make(self, text: str) -> str:
        """
        Method - interface for encrypting/decrypting input data.

        Args:
            text: the string to be encrypted or decrypted.

        Returns:
            Encrypted or decrypted string.
        """
        return self._transform(text)
