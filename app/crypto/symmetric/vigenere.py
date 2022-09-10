# This module contains the implementation of the cipher "Vigenere cipher"
import re

from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE
from ..common import EncProc
from ..exceptions import VigenereError


class Vigenere:
    def __init__(self, key: str):
        """
        Implementation of the symmetric Vigenère cipher.

        Args:
            key: a string consisting Russian or English alphabet.
        """
        if not key:
            raise VigenereError("The key is missing!")

        if not re.match(r"^[а-яёa-z]*$", key, re.IGNORECASE):
            raise VigenereError("Invalid key!")

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
            raise VigenereError("Input text is empty!")

        text_list: list[str] = list(text)

        for i in range(len(text)):
            letter_text = text_list[i]
            # Get the alphabet for the text character.
            if (lang_alphabet_text := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
                continue

            letter_key = self.key[i % len(self.key)]
            # # Get the alphabet for the key character.
            if (lang_alphabet_key := get_alphabet_by_letter(letter_key, ALPHABET_TABLE)) is None:
                continue

            _, alphabet_text = lang_alphabet_text
            _, alphabet_key = lang_alphabet_key

            letter_text_index = alphabet_text.index(letter_text.lower())
            letter_key_index = alphabet_key.index(letter_key.lower())

            # choice of sign
            match enc_proc:
                case EncProc.ENCRYPT:
                    key_sign = 1

                case EncProc.DECRYPT:
                    key_sign = -1

                case _:
                    raise VigenereError(f"Invalid processing type! -> {enc_proc}")

            new_letter_text_index = (letter_text_index + letter_key_index * key_sign) % len(alphabet_text)
            new_letter_text = alphabet_text[new_letter_text_index]

            if letter_text.isupper():
                new_letter_text = new_letter_text.upper()

            text_list[i] = new_letter_text

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
                If the data object is of a different type, then an exception will be raised VigenereError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise VigenereError(f"Invalid processing type! -> {enc_proc}")
