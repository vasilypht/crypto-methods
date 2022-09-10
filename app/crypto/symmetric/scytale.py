# This module contains the implementation of the cipher "Scytale cipher"
from app.crypto.common import EncProc
from ..exceptions import ScytaleError


class Scytale:
    def __init__(self, n: int, m: int = None, auto_m: bool = True):
        """
        Implementation of the symmetric cipher "Scytale".

        Args:
            n: a value that specifies the number of rows.
            m: a value that specifies the number of columns.
            auto_m: flag that determines the automatic calculation of the number of columns.
        """
        if not auto_m and m is None:
            raise ScytaleError("You must set the value of 'm', or set the automatic calculation flag 'auto_m'!")

        if n <= 0:
            raise ScytaleError("'n' must be positive!")

        if not auto_m:
            if m <= 0:
                raise ScytaleError("'n' must be positive!")

        self.n = n
        self.m = m
        self.auto_m = auto_m

    def encrypt(self, text: str) -> str:
        """
        Method - interface for encrypting input data.

        Args:
            text: the string to be encrypted.

        Returns:
            Encrypted string.
        """
        if not text:
            raise ScytaleError("Input text is empty!")

        if self.auto_m:
            self.m = (len(text) - 1) // self.n + 1

        lines_list: list[list[str]] = []

        # Breaking the line into blocks
        for i in range(self.n):
            line = list(text[i * self.m:(i + 1) * self.m])
            line += (self.m - len(line)) * [" "]
            lines_list.append(line)

        flip_lines_list = [i for i in zip(*lines_list)]
        return "".join("".join(i) for i in flip_lines_list)

    def decrypt(self, text: str) -> str:
        """
        Method - interface for decrypting input data.

        Args:
            text: the string to be decrypted.

        Returns:
            Decrypted string.
        """
        if not text:
            raise ScytaleError("Input text is empty!")

        lines_list: list[str] = []

        for i in range(self.n):
            line = text[i:len(text):self.n]
            lines_list.append(line)

        return "".join(lines_list)

    def make(self, text: str, enc_proc: EncProc = EncProc.ENCRYPT) -> str:
        """
        Method - interface for encrypting/decrypting input data.

        Args:
            text: the string to be encrypted or decrypted.

            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).
                If the data object is of a different type, then an exception will be raised ScytaleError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                raise ScytaleError(f"Invalid processing type! -> {enc_proc}")
