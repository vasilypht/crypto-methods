# This module contains the implementation of the cipher "Richelieu cipher"
import re

from ..common import EncProc


class RichelieuError(Exception):
    """The exception that is thrown when an error occurs in the Richelieu class"""
    pass


class Richelieu:
    def __init__(self, key: str):
        """
        Caesar class constructor.

        Args:
            key: a string of numbers combined into groups of brackets, example: (1,3,2,4)(4,2,1,3).
                If the sequence is violated or there are no brackets, or extra characters,
                then the RichelieuError exception will be raised.
        """
        if not key:
            raise RichelieuError("The key is missing!")

        if not re.match(r"^\(\d+(,\d+|\)\(\d+)*\)$", key):
            raise RichelieuError("Invalid key entered!")

        self.key = self._parse_key(key)
        pass

    @staticmethod
    def _parse_key(key: str) -> tuple:
        """Method for key parsing."""
        key_list = []
        for subkey in key.strip("()").split(")("):
            key_list.append(tuple(map(int, subkey.split(","))))

        # check range
        for subkey in key_list:
            for i in range(1, len(subkey) + 1):
                if i not in subkey:
                    raise RichelieuError("Invalid key entered!")

        return tuple(key_list)

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
            raise RichelieuError("Input text is empty!")

        text_list: list[str] = list(text)

        text_index = 0
        key_index = 0

        while True:
            subkey = self.key[key_index]

            if text_index + len(subkey) > len(text):
                break

            substr = text[text_index:text_index + len(subkey)]

            for i, k in enumerate(subkey):
                match enc_proc:
                    case EncProc.ENCRYPT:
                        text_list[text_index + k - 1] = substr[i]

                    case EncProc.DECRYPT:
                        text_list[text_index + i] = substr[k - 1]

                    case _:
                        raise RichelieuError(f"Invalid processing type! -> {enc_proc}")

            text_index += len(subkey)
            key_index = (key_index + 1) % len(self.key)

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
                If the data object is of a different type, then an exception will be raised RichelieuError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise RichelieuError(f"Invalid processing type! -> {enc_proc}")
