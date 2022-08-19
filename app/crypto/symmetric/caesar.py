from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE
from ..common import EncProc


class CaesarError(Exception):
    pass


class Caesar:
    def __init__(self, shift: int = 1):
        self.shift = shift

    def _transform(self, text: str, enc_proc: EncProc) -> str:
        """Caesar's cipher. Encryption/decryption function.

        Args:
            text: text to be encrypted/decrypted.

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise CaesarError("Input text is empty!")

        text_list: list[str] = list(text)

        for i in range(len(text)):
            letter_text = text_list[i]
            if (lang_alphabet := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
                continue

            _, alphabet = lang_alphabet
            letter_text_index = alphabet.index(letter_text.lower())

            # choice of sign
            match enc_proc:
                case EncProc.ENCRYPT:
                    sign = 1

                case EncProc.DECRYPT:
                    sign = -1

                case _:
                    raise CaesarError(f"Invalid processing type! -> {enc_proc}")

            new_letter_text_index = (letter_text_index + self.shift * sign) % len(alphabet)
            new_letter_text = alphabet[new_letter_text_index]

            if letter_text.isupper():
                new_letter_text = new_letter_text.upper()

            text_list[i] = new_letter_text

        return "".join(text_list)

    def encrypt(self, text: str) -> str:
        """Caesar cipher. Interface for calling encryption functions.

        Args:
            text: text to be encrypted.

        Returns:
            Encrypted string.
        """
        return self._transform(text, EncProc.ENCRYPT)

    def decrypt(self, text: str) -> str:
        """Caesar cipher. Interface for calling decryption functions.

        Args:
            text: text to be decrypted.

        Returns:
            Decrypted string.
        """
        return self._transform(text, EncProc.DECRYPT)

    def make(self, text: str, enc_proc: EncProc = EncProc.ENCRYPT) -> str:
        """Caesar cipher. Interface for calling encryption/decryption functions.

        Args:
            text: text to be encrypted/decrypted.

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
