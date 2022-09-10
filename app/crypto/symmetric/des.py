# This module contains the implementation of the cipher "DES"
from enum import (
    Enum,
    auto
)

from app.crypto.const import (
    DES_IP_TABLE, DES_IP_INV_TABLE,
    DES_PC_1_TABLE, DES_PC_2_TABLE,
    DES_E_TABLE, DES_P_TABLE,
    DES_S_TABLE, DES_SHIFT_TABLE
)
from app.crypto.common import EncProc
from ..exceptions import DESError


class DES:
    class EncMode(Enum):
        """Encryption Modes for DES."""
        ECB = auto()
        CBC = auto()
        CFB = auto()
        OFB = auto()

        @staticmethod
        def from_str(value: str):
            match value:
                case "ECB":
                    return DES.EncMode.ECB

                case "CBC":
                    return DES.EncMode.CBC

                case "CFB":
                    return DES.EncMode.CFB

                case "OFB":
                    return DES.EncMode.OFB

                case _:
                    raise NotImplementedError

    def __init__(self, key: str, iv: str = None, enc_mode: EncMode = EncMode.ECB, reset_iv: bool = True) -> None:
        """
        Implementation of the "DES" symmetric encryption algorithm. The following 
        encryption modes are available: ECB, CBC, CFB, OFB.

        Args:
            key: a string representing the 16th number. The key consists of 7 bytes,
                the string must have 14 characters. If the conditions are not met, an
                DESError exception will be raised.

            iv: a string representing the 16th number. The initialization vector
                consists of 8 bytes, the string must have 16 characters. If the conditions
                 are not met, an DESError exception will be raised.

            enc_mode: encryption mode, for this cipher there are several
                modes: ECB, CBC, CFB, OFB.

            reset_iv: parameter indicating whether to reset the initialization vector
                before encrypting/decrypting the input data.
        """
        if len(key) != 14:
            raise DESError(f"Key length must be 56 bits (7 bytes)! ({len(key) // 2} bytes entered)")

        try:
            self.key = int(key, 16)
        except ValueError:
            raise DESError("The entered key is not a hexadecimal value!")

        if iv:
            if len(iv) != 16:
                raise DESError(f"IV length must be 64 bits (8 bytes)! ({len(iv) // 2} bytes entered)")

            try:
                self.iv = int(iv, 16)
            except ValueError:
                raise DESError("The entered IV is not a hexadecimal value!")

            self.vector = self.iv

        if iv is None and enc_mode is not DES.EncMode.ECB:
            raise DESError(f"Encryption in '{enc_mode}' mode requires an initialization vector!")

        self._mode_fns = {DES.EncMode.ECB: self._ECB,
                          DES.EncMode.CBC: self._CBC,
                          DES.EncMode.CFB: self._CFB,
                          DES.EncMode.OFB: self._OFB}

        if enc_mode not in self._mode_fns.keys():
            raise DESError(f"Invalid encryption mode entered ({enc_mode})! "
                           f"Possible modes: {tuple(self._mode_fns.keys())}")

        self._mode_fn = self._mode_fns.get(enc_mode)
        self._reset_iv = reset_iv

        self.keys = self.generate_keys(self.key)

    def set_reset_iv_flag(self, flag: bool = False) -> None:
        """Method for setting the flag/clearing the flag by resetting the initialization vector."""
        self._reset_iv = flag

    def generate_keys(self, key: int) -> list[int]:
        """Method for generating encryption keys."""
        ext_key = 0

        # Getting a 64-bit key
        for i in range(8):
            k = (key >> (i * 7)) & 0b1111111

            match bin(k).count("1") % 2:
                case 0:
                    ext_key |= ((k << 1) | 0b1) << (8 * i)

                case 1:
                    ext_key |= ((k << 1) | 0b0) << (8 * i)

        new_key = self._permutation(ext_key, 64, DES_PC_1_TABLE)

        chunk_l = new_key >> 28
        chunk_d = new_key & 0xFFFFFFF
        keys = []

        for i in range(16):
            shift = DES_SHIFT_TABLE[i]

            chunk_l = ((chunk_l << shift) | (chunk_l >> (28 - shift))) & 0xFFFFFFF
            chunk_d = ((chunk_d << shift) | (chunk_d >> (28 - shift))) & 0xFFFFFFF

            block = (chunk_l << 28) | chunk_d
            new_key = self._permutation(block, 56, DES_PC_2_TABLE)
            keys.append(new_key)

        return keys

    @staticmethod
    def _permutation(key: int, bit_len: int, table: tuple) -> int:
        """Method for performing bit swapping on a table."""
        key = bin(key)[2:].zfill(bit_len)
        return int("".join(key[i - 1] for i in table), 2)

    def _transform(self, block: int, enc_proc: EncProc) -> int:
        """
        Data encryption/decryption method.

        Args:
            block: bytes converted to a number.
            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).

        Returns:
            Encrypted/decrypted block as a number.
        """
        block = self._permutation(block, 64, DES_IP_TABLE)
        chunk_l = block >> 32
        chunk_r = block & 0xFFFFFFFF

        match enc_proc:
            case EncProc.ENCRYPT:
                for i in range(16):
                    chunk_l, chunk_r = chunk_r, chunk_l ^ self._f(chunk_r, self.keys[i])

            case EncProc.DECRYPT:
                for i in range(15, -1, -1):
                    chunk_r, chunk_l = chunk_l, chunk_r ^ self._f(chunk_l, self.keys[i])

            case _:
                raise DESError(f"Invalid processing mode! -> {enc_proc}")

        block = (chunk_l << 32) | chunk_r
        return self._permutation(block, 64, DES_IP_INV_TABLE)

    def _f(self, chunk: int, key: int) -> int:
        """Method for calculating the Feistel function"""
        chunk = self._permutation(chunk, 32, DES_E_TABLE) ^ key

        new_chunk = 0
        for k in range(8):
            b = chunk >> (6 * k) & 0b111111
            i = ((b >> 5) << 1) | (b & 0b1)
            j = (b >> 1) & 0b1111
            new_chunk |= DES_S_TABLE[7 - k][i][j] << (6 * k)

        return self._permutation(new_chunk, 48, DES_P_TABLE)

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
                    raise DESError(f"Invalid processing mode! -> {enc_proc}")

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
                    raise DESError(f"Invalid processing mode! -> {enc_proc}")

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
                    raise DESError(f"Invalid processing mode! -> {enc_proc}")

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
                raise DESError(f"Invalid processing mode! -> {enc_proc}")

        if enc_proc is EncProc.ENCRYPT and (k := len(data_bytes) % 8) != 0:
            data_bytes += b"\00" * (8 - k)

        if self._reset_iv:
            self.vector = self.iv

        processed_data = self._mode_fn(data_bytes, enc_proc).rstrip(b'\00')

        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                return processed_data.hex()

            case EncProc.DECRYPT, str():
                return processed_data.decode("utf-8")

            case _, bytes():
                return processed_data

            case _:
                raise DESError(f"Invalid processing mode! -> {enc_proc}")

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
                raise DESError(f"Invalid processing mode! -> {enc_proc}")
