import numpy as np

from ..common import EncProc


class VernamError(Exception):
    pass


class Vernam:
    def __init__(self, key: str):
        try:
            self.key = bytes.fromhex(key)
        except ValueError:
            raise VernamError("Wrong format key entered (Hex)")

    @staticmethod
    def gen_key(size: int) -> str:
        sample = tuple(np.random.randint(0, 256, size))
        return bytes(sample).hex()

    def _transform(self, data: bytes or str, enc_proc: EncProc):
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

    def encrypt(self, data: str or bytes):
        return self._transform(data, EncProc.ENCRYPT)

    def decrypt(self, data: str or bytes):
        return self._transform(data, EncProc.DECRYPT)

    def make(self, data: str or bytes, enc_proc: EncProc = EncProc.ENCRYPT):
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(data)

            case EncProc.DECRYPT:
                return self.decrypt(data)

            case _:
                raise VernamError(f"Invalid processing mode! -> {enc_proc}")
