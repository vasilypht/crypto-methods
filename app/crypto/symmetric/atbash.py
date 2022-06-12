from ..utils import (
    get_alphabet_by_letter
)
from ..const import (
    ALPHABET_TABLE
)


class AtbashError(Exception):
    pass


class Atbash:
    def __init__(self):
        pass

    def _transform(self, text: str) -> str:
        """Atbash cipher. Encryption/decryption function.

        Args:
            text: text to be encrypted/decrypted.

        Returns:
            Encrypted or decrypted string.
        """

        if not text:
            raise AtbashError("Input text is empty!")

        letters_list: list[str] = list(text)

        for i in range(len(text)):
            letter_text = letters_list[i]

            if (lang_alphabet := get_alphabet_by_letter(letter_text, ALPHABET_TABLE)) is None:
                continue

            _, alphabet = lang_alphabet
            letter_index = alphabet.index(letter_text.lower())
            new_letter = alphabet[len(alphabet) - letter_index - 1]

            if letter_text.isupper():
                new_letter = new_letter.upper()

            letters_list[i] = new_letter

        return "".join(letters_list)

    def make(self, text: str) -> str:
        """Atbash cipher. Interface for calling encryption/decryption functions.

        Args:
            text: text to be encrypted/decrypted.

        Returns:
            Encrypted or decrypted string.
        """
        return self._transform(text)
