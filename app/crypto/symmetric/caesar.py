# This module contains the implementation of the cipher "Caesar's cipher"
from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE
from ..common import EncProc
from ..exceptions import CaesarError


class Caesar:
    def __init__(self, shift: int = 1) -> None:
        """
        Implementation of a symmetric Caesar cipher. 

        Args:
            shift: the value by which the letter in the alphabet will be shifted.
        """
        self.shift = shift

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
            raise CaesarError("Input text is empty!")

        text_list: list[str] = list(text)

        for i in range(len(text)):
            letter_text = text_list[i]

            # For each letter of the text, we look for the corresponding alphabet.
            # If there is none, we skip the iteration, skipping the given letter.
            if (lang_alphabet := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
                continue

            _, alphabet = lang_alphabet

            # Set the sign for encryption
            match enc_proc:
                case EncProc.ENCRYPT:
                    # The sign is positive, the shift value will be added
                    # to the character index
                    sign = 1

                case EncProc.DECRYPT:
                    # The sign is negative, the shift value will be subtracted
                    # from the character index
                    sign = -1

                case _:
                    raise CaesarError(f"Invalid processing type! -> {enc_proc}")

            # We get the index of the current letter and calculate the new index.
            letter_text_index = alphabet.index(letter_text.lower())
            new_letter_text_index = (letter_text_index + self.shift * sign) % len(alphabet)
            new_letter_text = alphabet[new_letter_text_index]

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
                If the data object is of a different type, then an exception will be raised CaesarError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise CaesarError(f"Invalid processing type! -> {enc_proc}")
