import re

from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE
from ..common import EncProc


class VigenereError(Exception):
    pass


class Vigenere:
    def __init__(self, key: str):
        if not key:
            raise VigenereError("The key is missing!")

        if not re.match(r"^[а-яА-ЯёЁa-zA-Z]*$", key):
            raise VigenereError("Invalid key!")

        self.key = key

    def _transform(self, text: str, enc_proc: EncProc) -> str:
        """Vigenere cipher. Encryption/Decryption function.

        Args:
            text: text to be encrypted/decrypted.
            enc_proc: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise VigenereError("Input text is empty!")

        text_list: list[str] = list(text)

        for i in range(len(text)):
            letter_text = text_list[i]
            if (lang_alphabet_text := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
                continue

            letter_key = self.key[i % len(self.key)]
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
        """Vigenere cipher. Interface for calling encryption functions.

        Args:
            text: text to be encrypted.

        Returns:
            Encrypted string.
        """
        return self._transform(text, EncProc.ENCRYPT)

    def decrypt(self, text: str) -> str:
        """Vigenere cipher. Interface for calling decryption functions.

        Args:
            text: text to be decrypted.

        Returns:
            Decrypted string.
        """
        return self._transform(text, EncProc.DECRYPT)

    def make(self, text: str, enc_proc: EncProc = EncProc.ENCRYPT) -> str:
        """Vigenere cipher. Interface for calling encryption/decryption functions.

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
                raise VigenereError(f"Invalid processing type! -> {enc_proc}")
