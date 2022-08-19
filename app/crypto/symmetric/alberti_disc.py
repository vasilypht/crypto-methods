import re

from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE
from ..common import EncProc


class AlbertiError(Exception):
    pass


class Alberti:
    def __init__(self, key: str, step: int = 0, shift: int = 0):
        if not key:
            raise AlbertiError("The key is missing!")

        if not re.match(r"(^[а-яё]*$)|(^[a-z]*$)", key, re.IGNORECASE):
            raise AlbertiError("Invalid key!")

        self.key = key

        if step < 0:
            raise AlbertiError("The step value must be positive or zero!")

        self.step = step

        if shift < 0:
            raise AlbertiError("The shift value must be positive or zero!")

        self.shift = shift

    def _transform(self, text: str, enc_proc: EncProc) -> str:
        if not text:
            raise AlbertiError("Input text is empty!")

        _, external_alphabet = get_alphabet_by_letter(self.key[0], ALPHABET_TABLE)

        internal_alphabet = ""
        for letter in self.key.lower() + external_alphabet:
            if letter not in internal_alphabet:
                internal_alphabet += letter

        # Making a shift in the internal alphabet
        internal_alphabet = internal_alphabet[self.shift::] + internal_alphabet[:self.shift:]

        match enc_proc:
            case EncProc.ENCRYPT:
                key_sign = 1

            case EncProc.DECRYPT:
                # swap alphabets
                internal_alphabet, external_alphabet = external_alphabet, internal_alphabet
                key_sign = -1

            case _:
                raise AlbertiError(f"Invalid processing type! -> {enc_proc}")

        text_list: list[str] = list(text)
        internal_shift = 0

        for i in range(len(text)):
            letter = text_list[i]

            if (letter_pos := external_alphabet.find(letter.lower())) == -1:
                continue

            new_letter_pos = (letter_pos + internal_shift) % len(internal_alphabet)
            new_letter = internal_alphabet[new_letter_pos]

            internal_shift = (internal_shift + self.step * key_sign) % len(internal_alphabet)

            if letter.isupper():
                new_letter = new_letter.upper()

            text_list[i] = new_letter

        return "".join(text_list)

    def encrypt(self, text: str) -> str:
        return self._transform(text, EncProc.ENCRYPT)

    def decrypt(self, text: str) -> str:
        return self._transform(text, EncProc.DECRYPT)

    def make(self, text: str, enc_proc: EncProc = EncProc.ENCRYPT) -> str:
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise AlbertiError(f"Invalid processing type! -> {enc_proc}")
