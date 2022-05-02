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

    def set_options(self, key: str):
        if not key:
            raise XORError("Key input value is empty!")

        try:
            self.key = bytes.fromhex(key)
        except ValueError:
            raise XORError("Wrong format key entered (Hex)")

    def _transform(self, data: bytes or str, mode: str = "encrypt", reset_state: bool = True):
        if mode not in ("encrypt", "decrypt"):
            raise XORError("The processing type does not match the allowed values! ('encrypt' or 'decrypt')")

        if not data:
            raise XORError("The input data is empty!")

        if not self.key:
            raise XORError("Encryption key not set!")

        # check input data
        match mode, data:
            case "encrypt", str():
                data_bytes = bytearray(data, "utf-8")

            case "decrypt", str():
                data_bytes = bytearray.fromhex(data)

            case _, bytes():
                data_bytes = bytearray(data)

            case _:
                raise XORError(f"Invalid processing type! -> {mode}")

        if reset_state:
            self.index_key = 0

        for i in range(len(data_bytes)):
            data_bytes[i] ^= self.key[self.index_key % len(self.key)]
            self.index_key = (self.index_key + 1) % len(self.key)

        # manage output
        match mode, data:
            case "encrypt", str():
                return data_bytes.hex()

            case "decrypt", str():
                return data_bytes.decode("utf-8")

            case _, bytes():
                return bytes(data_bytes)

            case _:
                raise XORError(f"Invalid processing type! -> {mode}")

    def encrypt(self, data: str or bytes, reset_state: bool = True):
        return self._transform(data, "encrypt", reset_state)

    def decrypt(self, data: str or bytes, reset_state: bool = True):
        return self._transform(data, "decrypt", reset_state)

    def make(self, data: str or bytes, mode: str = "encrypt", reset_state: bool = True):
        match mode:
            case "encrypt":
                return self._transform(data, "encrypt", reset_state)

            case "decrypt":
                return self._transform(data, "decrypt", reset_state)

            case _:
                raise XORError(f"Wrong encryption mode! ({mode})")
