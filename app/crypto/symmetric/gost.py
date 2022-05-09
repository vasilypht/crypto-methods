from app.crypto.const import (
    GOST_ENC_INDICES,
    GOST_DEC_INDICES,
    GOST_SBLOCK
)


class GOSTError(Exception):
    pass


class GOST:
    def __init__(self, key: str, iv: str = None, mode: str = "ECB"):
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

        if iv is None and mode != "ECB":
            raise GOSTError(f"Encryption in '{mode}' mode requires an initialization vector!")

        self.subkeys = tuple((self.key >> (32 * i)) & 0xFFFFFFFF for i in range(8))

        self._modes = {"ECB": self._ECB,
                       "CBC": self._CBC,
                       "CFB": self._CFB,
                       "OFB": self._OFB}

        self._mode = self._modes.get(mode)

    def _transform(self, block: int, mode: str = "encrypt"):
        chunk_l = block >> 32
        chunk_r = block & 0xFFFFFFFF

        match mode:
            case "encrypt":
                indices = GOST_ENC_INDICES

            case "decrypt":
                indices = GOST_DEC_INDICES

            case _:
                raise GOSTError(f"Invalid processing mode! -> {mode}")

        for i in indices:
            chunk_l, chunk_r = chunk_r ^ self._f(chunk_l, self.subkeys[i]), chunk_l

        return (chunk_r << 32) | chunk_l

    def _f(self, chunk: int, key: int):
        k = (chunk + key) % 4_294_967_296

        new_chunk = 0
        for i in range(8):
            new_chunk |= GOST_SBLOCK[7 - i][(k >> (4 * i)) & 0b1111] << (4 * i)

        return ((new_chunk << 11) | (new_chunk >> 21)) & 0xFFFFFFFF

    def _ECB(self, data: bytes, mode: str = "encrypt"):
        processed_data = bytes()

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")
            processed_block = self._transform(block, mode)
            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _CBC(self, data: bytes, mode: str = "encrypt"):
        processed_data = bytes()
        vector = self.iv

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")

            match mode:
                case "encrypt":
                    processed_block = self._transform(block ^ vector, "encrypt")
                    vector = processed_block

                case "decrypt":
                    processed_block = self._transform(block, "decrypt") ^ vector
                    vector = block

                case _:
                    raise GOSTError(f"Invalid processing mode! -> {mode}")

            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _CFB(self, data: bytes, mode: str = "encrypt"):
        processed_data = bytes()
        vector = self.iv

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")

            match mode:
                case "encrypt":
                    processed_block = self._transform(vector, "encrypt") ^ block
                    vector = processed_block

                case "decrypt":
                    processed_block = self._transform(vector, "encrypt") ^ block
                    vector = block

                case _:
                    raise GOSTError(f"Invalid processing mode! -> {mode}")

            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _OFB(self, data: bytes, mode: str = "encrypt"):
        processed_data = bytes()
        vector = self.iv

        for pos in range(0, len(data), 8):
            block = int.from_bytes(data[pos:pos + 8], "little")

            match mode:
                case "encrypt":
                    vector = self._transform(vector, "encrypt")
                    processed_block = vector ^ block

                case "decrypt":
                    vector = self._transform(vector, "encrypt")
                    processed_block = vector ^ block

                case _:
                    raise GOSTError(f"Invalid processing mode! -> {mode}")

            processed_data += processed_block.to_bytes(8, "little")

        return processed_data

    def _data_processing(self, data: bytes or str, mode: str = "encrypt"):
        match mode, data:
            case "encrypt", str():
                data_bytes = data.encode("utf-8")

            case "decrypt", str():
                data_bytes = bytes.fromhex(data)

            case _, bytes():
                data_bytes = data

            case _:
                raise GOSTError(f"Invalid processing mode! -> {mode}")

        # The size of one block is 64 bits -> 8 bytes
        # Check if the number of bytes is a multiple of the block size
        if mode == "encrypt" and (k := len(data_bytes) % 8) != 0:
            data_bytes += b"\00" * (8 - k)

        processed_data = self._mode(data_bytes, mode)

        match mode, data:
            case "encrypt", str():
                return processed_data.hex()

            case "decrypt", str():
                return processed_data.decode("utf-8")

            case _, bytes():
                return processed_data

            case _:
                raise GOSTError(f"Invalid processing mode! -> {mode}")

    def encrypt(self, data: bytes or str):
        return self._data_processing(data, "encrypt")

    def decrypt(self, data: bytes or str):
        return self._data_processing(data, "decrypt")

    def make(self, data: bytes or str, mode: str = "encrypt"):
        match mode:
            case "encrypt":
                return self.encrypt(data)

            case "decrypt":
                return self.decrypt(data)

            case _:
                raise GOSTError(f"Invalid processing mode! -> {mode}")
