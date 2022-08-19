from ..common import EncProc


class XORError(Exception):
    pass


class XOR:
    def __init__(self, key: str):
        if not key:
            raise XORError("Key input value is empty!")

        try:
            self.key = bytes.fromhex(key)
        except ValueError:
            raise XORError("Wrong format key entered (Hex)")

        self.index_key = 0

    def _transform(self, data: bytes or str, enc_proc: EncProc, reset_state: bool = True):
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

        if reset_state:
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

    def encrypt(self, data: str or bytes, reset_state: bool = True):
        return self._transform(data, EncProc.ENCRYPT, reset_state)

    def decrypt(self, data: str or bytes, reset_state: bool = True):
        return self._transform(data, EncProc.DECRYPT, reset_state)

    def make(self, data: str or bytes, enc_proc: EncProc = EncProc.ENCRYPT, reset_state: bool = True):
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(data, reset_state)

            case EncProc.DECRYPT:
                return self.decrypt(data, reset_state)

            case _:
                raise XORError(f"Wrong encryption mode! ({enc_proc})")
