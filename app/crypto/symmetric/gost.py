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


class EncMode(Enum):
    ECB = auto()
    CBC = auto()
    CFB = auto()
    OFB = auto()

    @staticmethod
    def from_str(value: str):
        match value:
            case "ECB":
                return EncMode.ECB

            case "CBC":
                return EncMode.CBC

            case "CFB":
                return EncMode.CFB

            case "OFB":
                return EncMode.OFB

            case _:
                raise NotImplementedError


class GOSTError(Exception):
    pass


class GOST:
    def __init__(self, key: str, iv: str = None, enc_mode: EncMode = EncMode.ECB):
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

        if iv is None and enc_mode is not EncMode.ECB:
            raise GOSTError(f"Encryption in '{enc_mode}' mode requires an initialization vector!")

        self.subkeys = tuple((self.key >> (32 * i)) & 0xFFFFFFFF for i in range(8))

        self._modes = {EncMode.ECB: self._ECB,
                       EncMode.CBC: self._CBC,
                       EncMode.CFB: self._CFB,
                       EncMode.OFB: self._OFB}

        self._fn_mode = self._modes.get(enc_mode)

    def _transform(self, block: int, enc_proc: EncProc):
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

    def _f(self, chunk: int, key: int):
        k = (chunk + key) % 4_294_967_296

        new_chunk = 0
        for i in range(8):
            new_chunk |= GOST_SBLOCK[7 - i][(k >> (4 * i)) & 0b1111] << (4 * i)

        return ((new_chunk << 11) | (new_chunk >> 21)) & 0xFFFFFFFF

    def _ECB(self, data: bytes, enc_proc: EncProc):
        processed_data = bytes()

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")
            processed_block = self._transform(block, enc_proc)
            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _CBC(self, data: bytes, enc_proc: EncProc):
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

    def _CFB(self, data: bytes, enc_proc: EncProc):
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

    def _OFB(self, data: bytes, enc_proc: EncProc):
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

    def _data_processing(self, data: bytes or str, enc_proc: EncProc, reset_iv: bool = True):
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

        if reset_iv:
            self.vector = self.iv

        processed_data = self._fn_mode(data_bytes, enc_proc)

        match enc_proc, data:
            case EncProc.ENCRYPT, str():
                return processed_data.hex()

            case EncProc.DECRYPT, str():
                return processed_data.decode("utf-8")

            case _, bytes():
                return processed_data

            case _:
                raise GOSTError(f"Invalid processing mode! -> {enc_proc}")

    def encrypt(self, data: bytes or str, reset_iv: bool = True):
        return self._data_processing(data, EncProc.ENCRYPT, reset_iv)

    def decrypt(self, data: bytes or str, reset_iv: bool = True):
        return self._data_processing(data, EncProc.DECRYPT, reset_iv)

    def make(self, data: bytes or str, enc_proc: EncProc = EncProc.ENCRYPT, reset_iv: bool = True):
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(data, reset_iv)

            case EncProc.DECRYPT:
                return self.decrypt(data, reset_iv)

            case _:
                raise GOSTError(f"Invalid processing mode! -> {enc_proc}")
