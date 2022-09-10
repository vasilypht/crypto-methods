# This module contains the implementation of the cipher "XOR cipher"
from ..common import EncProc
from ..exceptions import XORError


class XOR:
    def __init__(self, key: str, reset_state: bool = True):
        """
        Implementation of the symmetric cipher "XOR".

        Args:
            key: a string representing the 16th number.
            reset_state: parameter indicating whether to reset the state before
                encrypting/decrypting the input data.
        """
        if not key:
            raise XORError("Key input value is empty!")

        try:
            self.key = bytes.fromhex(key)
        except ValueError:
            raise XORError("Wrong format key entered (Hex)")

        self._reset_state = reset_state

        self.index_key = 0

    def set_reset_state_flag(self, flag: bool = False):
        """Method for setting the flag/clearing the flag by resetting the state."""
        self._reset_state = flag

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
            raise XORError("The input data is empty!")

        # check input data
        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                data_bytes = bytearray(data, "utf-8")

            case EncProc.DECRYPT, str():
                data_bytes = bytearray.fromhex(data)

            case _, bytes():
                data_bytes = bytearray(data)

            case _:
                raise XORError(f"Invalid processing type! -> {enc_proc}")

        if self._reset_state:
            self.index_key = 0

        for i in range(len(data_bytes)):
            data_bytes[i] ^= self.key[self.index_key % len(self.key)]
            self.index_key = (self.index_key + 1) % len(self.key)

        # manage output
        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                return data_bytes.hex()

            case EncProc.DECRYPT, str():
                return data_bytes.decode("utf-8")

            case _, bytes():
                return bytes(data_bytes)

            case _:
                raise XORError(f"Invalid processing type! -> {enc_proc}")

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
                raise XORError(f"Wrong encryption mode! ({enc_proc})")
