# This module contains the implementation of the cipher "Alberti's Disk"
import re

from ..utils import get_alphabet_by_letter
from ..const import ALPHABET_TABLE
from ..common import EncProc
from ..exceptions import AlbertiError


class Alberti:
    def __init__(self, key: str, step: int = 0, shift: int = 0) -> None:
        """
        Implementation of the symmetric cipher "Alberti's Disk".

        Args:
            key: a string containing only characters of the English alphabet, or only the Russian alphabet.
                It is allowed to use key characters in different case. If the key contains numbers, special
                characters, or characters from other alphabets, then the AlbertiError exception will be raised.

            step: encryption step. The value by which the disk will be shifted after each iteration.
                This value must be positive. If this value is negative, an AlbertiError exception will be thrown.

            shift: initial shift of the internal alphabet. This value must be positive. If this value
                is negative, an AlbertiError exception will be thrown.
        """
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
        """
        Data encryption/decryption method.

        Args:
            text: the string to be encrypted or decrypted.

            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise AlbertiError("Input text is empty!")

        # Since the alphabet consists of letters of the same alphabet,
        # we get the alphabet by the first letter of the key.
        _, external_alphabet = get_alphabet_by_letter(self.key[0], ALPHABET_TABLE)

        # We form the internal alphabet - the key + the remaining letters of the alphabet.
        internal_alphabet = ""
        for letter in self.key.lower() + external_alphabet:
            # We add letters from the key, excluding repetitions, and then
            # supplement with letters from the alphabet.
            if letter not in internal_alphabet:
                internal_alphabet += letter

        # Shifting the internal alphabet to the right.
        internal_alphabet = internal_alphabet[self.shift::] + internal_alphabet[:self.shift:]

        match enc_proc:
            case EncProc.ENCRYPT:
                # The encryption process will be carried out by shifting the internal alphabet to the right.
                key_sign = 1

            case EncProc.DECRYPT:
                # The decryption process will take place by shifting the internal alphabet to the left,
                # that is, the reverse process. To do this, swap the internal and external disks.
                internal_alphabet, external_alphabet = external_alphabet, internal_alphabet
                key_sign = -1

            case _:
                raise AlbertiError(f"Invalid processing type! -> {enc_proc}")

        text_list: list[str] = list(text)
        internal_shift = 0

        for i in range(len(text)):
            letter = text_list[i]

            # We are looking for letters of the internal alphabet on an external disk.
            # If the position is -1, then the character does not belong to the alphabet - we skip the iteration.
            if (letter_pos := external_alphabet.find(letter.lower())) == -1:
                continue

            # We consider a new position taking into account the shift of the alphabet.
            new_letter_pos = (letter_pos + internal_shift) % len(internal_alphabet)
            new_letter = internal_alphabet[new_letter_pos]

            # Update the alphabet shift value.
            internal_shift = (internal_shift + self.step * key_sign) % len(internal_alphabet)

            if letter.isupper():
                new_letter = new_letter.upper()

            text_list[i] = new_letter

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
                If the data object is of a different type, then an exception will be raised AlbertiError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise AlbertiError(f"Invalid processing type! -> {enc_proc}")
