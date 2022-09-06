# This module contains the implementation of the cipher "GOST 28147-89"
from enum import (
    Enum,
    auto
)

from app.crypto.const import (
    GOST_ENC_INDICES,
    GOST_DEC_INDICES,
    GOST_SBLOCK
)
from app.crypto.common import EncProc
from ..exceptions import GOSTError


class GOST:
    class EncMode(Enum):
        """Encryption Modes for GOST 28147-89."""
        ECB = auto()
        CBC = auto()
        CFB = auto()
        OFB = auto()

        @staticmethod
        def from_str(value: str):
            match value:
                case "ECB":
                    return GOST.EncMode.ECB

                case "CBC":
                    return GOST.EncMode.CBC

                case "CFB":
                    return GOST.EncMode.CFB

                case "OFB":
                    return GOST.EncMode.OFB

                case _:
                    raise NotImplementedError

    def __init__(self, key: str, iv: str = None, enc_mode: EncMode = EncMode.ECB, reset_iv: bool = True) -> None:
        """
        GOST class constructor.

        Args:
            key: a string representing the 16th number. The key consists of 32 bytes,
                the string must have 64 characters. If the conditions are not met, an
                GOSTError exception will be raised.

            iv: a string representing the 16th number. The initialization vector
                consists of 8 bytes, the string must have 16 characters. If the conditions
                are not met, an GOSTError exception will be raised.

            enc_mode: encryption mode, for this cipher there are several
                modes: ECB, CBC, CFB, OFB.

            reset_iv: parameter indicating whether to reset the initialization vector
                before encrypting/decrypting the input data.
        """
        if len(key) != 64:
            raise GOSTError(f"Key length must be 256 bits (32 bytes)! ({len(key) // 2} bytes entered)")

        try:
            self.key = int(key, 16)
        except ValueError:
            raise GOSTError("The entered key is not a hexadecimal value!")

        if iv:
            if len(iv) != 16:
                raise GOSTError(f"IV length must be 64 bits (8 bytes)! ({len(iv) // 2} bytes entered)")

            try:
                self.iv = int(iv, 16)
            except ValueError:
                raise GOSTError("The entered IV is not a hexadecimal value!")

            self.vector = self.iv

        if iv is None and enc_mode is not GOST.EncMode.ECB:
            raise GOSTError(f"Encryption in '{enc_mode}' mode requires an initialization vector!")

        # Generation of encryption keys.
        self.subkeys = tuple((self.key >> (32 * i)) & 0xFFFFFFFF for i in range(8))

        self._mode_fns = {GOST.EncMode.ECB: self._ECB,
                          GOST.EncMode.CBC: self._CBC,
                          GOST.EncMode.CFB: self._CFB,
                          GOST.EncMode.OFB: self._OFB}

        if enc_mode not in self._mode_fns.keys():
            raise GOSTError(f"Invalid encryption mode entered ({enc_mode})! "
                            f"Possible modes: {tuple(self._mode_fns.keys())}")

        self._mode_fn = self._mode_fns.get(enc_mode)
        self._reset_iv = reset_iv

    def set_reset_iv_flag(self, flag: bool = False) -> None:
        """Method for setting the flag/clearing the flag by resetting the initialization vector."""
        self._reset_iv = flag

    def _transform(self, block: int, enc_proc: EncProc) -> int:
        """
        Data encryption/decryption method.

        Args:
            block: bytes converted to a number.
            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).

        Returns:
            Encrypted/decrypted block as a number.
        """
        chunk_l = block >> 32
        chunk_r = block & 0xFFFFFFFF

        match enc_proc:
            case EncProc.ENCRYPT:
                indices = GOST_ENC_INDICES

            case EncProc.DECRYPT:
                indices = GOST_DEC_INDICES

            case _:
                raise GOSTError(f"Invalid processing mode! -> {enc_proc}")

        for i in indices:
            chunk_l, chunk_r = chunk_r ^ self._f(chunk_l, self.subkeys[i]), chunk_l

        return (chunk_r << 32) | chunk_l

    def _f(self, chunk: int, key: int) -> int:
        """Method for calculating the Feistel function"""
        k = (chunk + key) % 4_294_967_296

        new_chunk = 0
        for i in range(8):
            new_chunk |= GOST_SBLOCK[7 - i][(k >> (4 * i)) & 0b1111] << (4 * i)

        return ((new_chunk << 11) | (new_chunk >> 21)) & 0xFFFFFFFF

    def _ECB(self, data: bytes, enc_proc: EncProc) -> bytes:
        """Method for processing data in ECB mode"""
        processed_data = bytes()

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")
            processed_block = self._transform(block, enc_proc)
            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _CBC(self, data: bytes, enc_proc: EncProc) -> bytes:
        """Method for processing data in CBC mode"""
        processed_data = bytes()

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")

            match enc_proc:
                case EncProc.ENCRYPT:
                    processed_block = self._transform(block ^ self.vector, EncProc.ENCRYPT)
                    self.vector = processed_block

                case EncProc.DECRYPT:
                    processed_block = self._transform(block, EncProc.DECRYPT) ^ self.vector
                    self.vector = block

                case _:
                    raise GOSTError(f"Invalid processing mode! -> {enc_proc}")

            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _CFB(self, data: bytes, enc_proc: EncProc) -> bytes:
        """Method for processing data in CFB mode"""
        processed_data = bytes()

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")

            match enc_proc:
                case EncProc.ENCRYPT:
                    processed_block = self._transform(self.vector, EncProc.ENCRYPT) ^ block
                    self.vector = processed_block

                case EncProc.DECRYPT:
                    processed_block = self._transform(self.vector, EncProc.ENCRYPT) ^ block
                    self.vector = block

                case _:
                    raise GOSTError(f"Invalid processing mode! -> {enc_proc}")

            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _OFB(self, data: bytes, enc_proc: EncProc) -> bytes:
        """Method for processing data in OFB mode"""
        processed_data = bytes()

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")

            match enc_proc:
                case EncProc.ENCRYPT:
                    self.vector = self._transform(self.vector, EncProc.ENCRYPT)
                    processed_block = self.vector ^ block

                case EncProc.DECRYPT:
                    self.vector = self._transform(self.vector, EncProc.ENCRYPT)
                    processed_block = self.vector ^ block

                case _:
                    raise GOSTError(f"Invalid processing mode! -> {enc_proc}")

            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _data_processing(self, data: bytes or str, enc_proc: EncProc) -> str or bytes:
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
        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                data_bytes = data.encode("utf-8")

            case EncProc.DECRYPT, str():
                data_bytes = bytes.fromhex(data)

            case _, bytes():
                data_bytes = data

            case _:
                raise GOSTError(f"Invalid processing mode! -> {enc_proc}")

        # The size of one block is 64 bits -> 8 bytes
        # Check if the number of bytes is a multiple of the block size
        if enc_proc is EncProc.ENCRYPT and (k := len(data_bytes) % 8) != 0:
            data_bytes += b"\00" * (8 - k)

        if self._reset_iv:
            self.vector = self.iv

        processed_data = self._mode_fn(data_bytes, enc_proc).rstrip(b"\00")

        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                return processed_data.hex()

            case EncProc.DECRYPT, str():
                return processed_data.decode("utf-8")

            case _, bytes():
                return processed_data

            case _:
                raise GOSTError(f"Invalid processing mode! -> {enc_proc}")

    def encrypt(self, data: bytes or str) -> str or bytes:
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
        return self._data_processing(data, EncProc.ENCRYPT)

    def decrypt(self, data: bytes or str) -> str or bytes:
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
        return self._data_processing(data, EncProc.DECRYPT)

    def make(self, data: bytes or str, enc_proc: EncProc = EncProc.ENCRYPT) -> str or bytes:
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
                raise GOSTError(f"Invalid processing mode! -> {enc_proc}")
