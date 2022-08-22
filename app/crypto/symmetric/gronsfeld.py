# This module contains the implementation of the cipher "Gronsfeld cipher"
import re

from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE
from ..common import EncProc
from ..exceptions import GronsfeldError


class Gronsfeld:
    def __init__(self, key: str) -> None:
        """
        Gronsfeld class constructor.

        Args:
            key: a string of numbers. If the condition is not met, an GronsfeldError exception will be raised.
        """
        if not key:
            raise GronsfeldError("The key is missing!")

        if not re.match(r"^\d*$", key):
            raise GronsfeldError("Invalid key!")

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
            raise GronsfeldError("Input text is empty!")

        text_list: list[str] = list(text)

        for i in range(len(text)):
            letter_text = text_list[i]

            # For each letter of the text, we look for the corresponding alphabet.
            # If there is none, we skip the iteration, skipping the given letter.
            if (lang_alphabet := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
                continue

            _, alphabet = lang_alphabet
            shift = int(self.key[i % len(self.key)])

            # Set the sign for encryption
            match enc_proc:
                case EncProc.ENCRYPT:
                    sign = 1

                case EncProc.DECRYPT:
                    sign = -1

                case _:
                    raise GronsfeldError(f"Invalid processing type! -> {enc_proc}")

            # We get the index of the current letter and calculate the new index.
            letter_text_index = alphabet.index(letter_text.lower())
            new_letter_index = (letter_text_index + shift * sign) % len(alphabet)
            new_letter_text = alphabet[new_letter_index]

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
                If the data object is of a different type, then an exception will be raised GronsfeldError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise GronsfeldError(f"Invalid processing type! -> {enc_proc}")
