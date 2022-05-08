from src.crypto.const import (
    DES_IP_TABLE, DES_IP_INV_TABLE,
    DES_PC_1_TABLE, DES_PC_2_TABLE,
    DES_E_TABLE, DES_P_TABLE,
    DES_S_TABLE, DES_SHIFT_TABLE
)


class DESError(Exception):
    pass


class DES:
    def __init__(self, key: str, iv: str = None, mode: str = "ECB"):
        self._modes = {"ECB": self._ECB,
                       "CBC": self._CBC,
                       "CFB": self._CFB,
                       "OFB": self._OFB}

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

        if iv is None and mode != "ECB":
            raise DESError(f"Encryption in '{mode}' mode requires an initialization vector!")

        if mode not in self._modes.keys():
            raise DESError(f"Invalid encryption mode entered ({mode})! "
                           f"Possible modes: {tuple(self._modes.keys())}")

        self._mode = self._modes.get(mode)
        self.keys = self.generate_keys(self.key)

    def generate_keys(self, key: int):
        ext_key = 0

        # Getting a 64-bit key
        for i in range(8):
            k = (key >> (i * 7)) & 0b1111111

            match bin(k).count("1") % 2:
                case 0:
                    ext_key |= ((k << 1) | 0b1) << (8 * i)

                case 1:
                    ext_key |= ((k << 1) | 0b0) << (8 * i)

        # Permutation
        new_key = self._permutation(ext_key, 64, DES_PC_1_TABLE)

        chunk_l = new_key >> 28
        chunk_d = new_key & 0xFFFFFFF
        keys = []

        for i in range(16):
            shift = DES_SHIFT_TABLE[i]

            chunk_l = ((chunk_l << shift) | (chunk_l >> (28 - shift))) & 0xFFFFFFF
            chunk_d = ((chunk_d << shift) | (chunk_d >> (28 - shift))) & 0xFFFFFFF

            # Final permutation
            block = (chunk_l << 28) | chunk_d
            new_key = self._permutation(block, 56, DES_PC_2_TABLE)
            keys.append(new_key)

        return keys

    def _permutation(self, key: int, bit_len: int, table: tuple):
        key = bin(key)[2:].zfill(bit_len)
        return int("".join(key[i - 1] for i in table), 2)

    def _transform(self, block: int, mode: str = "encrypt"):
        block = self._permutation(block, 64, DES_IP_TABLE)
        chunk_l = block >> 32
        chunk_r = block & 0xFFFFFFFF

        match mode:
            case "encrypt":
                for i in range(16):
                    chunk_l, chunk_r = chunk_r, chunk_l ^ self._f(chunk_r, self.keys[i])

            case "decrypt":
                for i in range(15, -1, -1):
                    chunk_r, chunk_l = chunk_l, chunk_r ^ self._f(chunk_l, self.keys[i])

            case _:
                raise DESError(f"Invalid processing mode! -> {mode}")

        block = (chunk_l << 32) | chunk_r
        return self._permutation(block, 64, DES_IP_INV_TABLE)

    def _f(self, chunk: int, key: int):
        chunk = self._permutation(chunk, 32, DES_E_TABLE) ^ key

        new_chunk = 0
        for k in range(8):
            b = chunk >> (6 * k) & 0b111111
            i = ((b >> 5) << 1) | (b & 0b1)
            j = (b >> 1) & 0b1111
            new_chunk |= DES_S_TABLE[7 - k][i][j] << (6 * k)

        return self._permutation(new_chunk, 48, DES_P_TABLE)

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
                    raise DESError(f"Invalid processing mode! -> {mode}")

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
                    raise DESError(f"Invalid processing mode! -> {mode}")

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
                    raise DESError(f"Invalid processing mode! -> {mode}")

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
                raise DESError(f"Invalid processing mode! -> {mode}")

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
                raise DESError(f"Invalid processing mode! -> {mode}")

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
                raise DESError(f"Invalid processing mode! -> {mode}")
