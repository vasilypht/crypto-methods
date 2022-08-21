# This module contains the implementation of the cipher "Vernam"
import numpy as np

from ..common import EncProc


class VernamError(Exception):
    """The exception that is thrown when an error occurs in the Vernam class"""
    pass


class Vernam:
    def __init__(self, key: str) -> None:
        """
        Vernam class constructor.

        Args:
            key: a string representing the 16th number.
        """
        try:
            self.key = bytes.fromhex(key)
        except ValueError:
            raise VernamError("Wrong format key entered (Hex)")

    @staticmethod
    def gen_key(size: int) -> str:
        """Method for generating a key."""
        sample = tuple(np.random.randint(0, 256, size))
        return bytes(sample).hex()

    def _transform(self, data: bytes or str, enc_proc: EncProc) -> str or bytes:
        """
        Method for processing data. This method converts the input data to bytes,
        then conversions are performed and the output data is converted to a specific type.

        * If the input is a string and the encryption mode, then the output will
          be a string containing data in hexadecimal mode.

        * If the input is bytes and the encryption or decryption mode, then the output will be bytes.

        * If the input is a string (hex) and the decryption mode, then the output will be a
          string with data in utf-8

        Args:
            data: bytes or string to be encrypted/decrypted.
            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).

        Returns:
            Encrypted or decrypted strings or bytes.
        """
        if not data:
            raise VernamError("The input data is empty!")

        # check input data
        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                data_bytes = bytearray(data, "utf-8")

            case EncProc.DECRYPT, str():
                data_bytes = bytearray.fromhex(data)

            case _, bytes():
                data_bytes = bytearray(data)

            case _:
                raise VernamError(f"Invalid processing type! -> {enc_proc}")

        if len(self.key) != len(data_bytes):
            raise VernamError(f"Key size ({len(self.key)}) and text size ({len(data_bytes)}) in bytes must match!")

        for i in range(len(data_bytes)):
            data_bytes[i] ^= self.key[i % len(self.key)]

        # manage output
        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                return data_bytes.hex()

            case EncProc.DECRYPT, str():
                return data_bytes.decode("utf-8")

            case _, bytes():
                return bytes(data_bytes)

            case _:
                raise VernamError(f"Invalid processing type! -> {enc_proc}")

    def encrypt(self, data: str or bytes) -> str or bytes:
        """
        Method - interface for encrypting input data.

        * If the input is a string and the encryption mode, then the output will
          be a string containing data in hexadecimal mode.

        * If the input is bytes and the encryption mode, then the output will be bytes.

        Args:
            data: bytes or string to be encrypted.

        Returns:
            Encrypted strings or bytes.
        """
        return self._transform(data, EncProc.ENCRYPT)

    def decrypt(self, data: str or bytes) -> str or bytes:
        """
        Method - interface for encrypting input data.

        * If the input is bytes and the decryption mode, then the output will be bytes.

        * If the input is a string (hex) and the decryption mode, then the output will be a
          string with data in utf-8

        Args:
            data: bytes or string to be decrypted.

        Returns:
            Decrypted strings or bytes.
        """
        return self._transform(data, EncProc.DECRYPT)

    def make(self, data: str or bytes, enc_proc: EncProc = EncProc.ENCRYPT) -> str or bytes:
        """
        Method - interface for encrypting/decrypting input data.

        * If the input is a string and the encryption mode, then the output will
          be a string containing data in hexadecimal mode.

        * If the input is bytes and the encryption or decryption mode, then the output will be bytes.

        * If the input is a string (hex) and the decryption mode, then the output will be a
          string with data in utf-8

        Args:
            data: bytes or string to be encrypted/decrypted.
            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).

        Returns:
            Encrypted or decrypted strings or bytes.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(data)

            case EncProc.DECRYPT:
                return self.decrypt(data)

            case _:
                raise VernamError(f"Invalid processing mode! -> {enc_proc}")
