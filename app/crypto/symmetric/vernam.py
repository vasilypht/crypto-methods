import numpy as np


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

    def _transform(self, data: bytes or str, mode: str = "encrypt"):
        if mode not in ("encrypt", "decrypt"):
            raise VernamError("The processing type does not match the allowed values! ('encrypt' or 'decrypt')")

        if not data:
            raise VernamError("The input data is empty!")

        if not self.key:
            raise VernamError("Encryption key not set!")

        # check input data
        match mode, data:
            case "encrypt", str():
                data_bytes = bytearray(data, "utf-8")

            case "decrypt", str():
                data_bytes = bytearray.fromhex(data)

            case _, bytes():
                data_bytes = bytearray(data)

            case _:
                raise VernamError(f"Invalid processing type! -> {mode}")

        if len(self.key) != len(data_bytes):
            raise VernamError(f"Key size ({len(self.key)}) and text size ({len(data_bytes)}) in bytes must match!")

        for i in range(len(data_bytes)):
            data_bytes[i] ^= self.key[i % len(self.key)]

        # manage output
        match mode, data:
            case "encrypt", str():
                return data_bytes.hex()

            case "decrypt", str():
                return data_bytes.decode("utf-8")

            case _, bytes():
                return bytes(data_bytes)

            case _:
                raise VernamError(f"Invalid processing type! -> {mode}")

    def encrypt(self, data: str or bytes):
        return self._transform(data, "encrypt")

    def decrypt(self, data: str or bytes):
        return self._transform(data, "decrypt")
