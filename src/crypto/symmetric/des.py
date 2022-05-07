from bitarray import bitarray
from bitarray.util import (
    hex2ba, ba2hex,
    int2ba, ba2int,
    parity, zeros
)

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

        try:
            self.key = hex2ba(key)
        except ValueError:
            raise DESError("The entered key is not a hexadecimal one!")

        if len(self.key) != 56:
            raise DESError(f"Key length must be 56 bits (7 bytes)! ({len(self.key)} bits entered)")

        if iv:
            try:
                self.iv = hex2ba(iv)
            except ValueError:
                raise DESError("The entered IV is not a hexadecimal one!")

            if len(self.iv) != 64:
                raise DESError(f"IV length must be 64 bits (8 bytes)! ({len(self.iv)} bits entered)")

        if iv is None and mode != "ECB":
            raise DESError(f"Encryption in '{mode}' mode requires an initialization vector!")

        if mode not in self._modes.keys():
            raise DESError(f"Invalid encryption mode entered ({mode})! "
                           f"Possible modes: {tuple(self._modes.keys())}")

        self._mode = self._modes.get(mode)
        self.keys = self.generate_keys(self.key)

    def generate_keys(self, key: bitarray):
        ext_key = key.copy()

        # Getting a 64-bit key
        for pos in range(0, 64, 8):
            match parity(ext_key[pos:pos + 7]):
                case 0:
                    ext_key.insert(pos + 8, 1)

                case 1:
                    ext_key.insert(pos + 8, 0)

        # Permutation
        new_key = self._permutation(ext_key, DES_PC_1_TABLE)

        chunk_l, chunk_d = new_key[:28], new_key[28:]
        keys = []

        for i in range(16):
            shift = DES_SHIFT_TABLE[i]

            addition_l, addition_d = chunk_l[:shift], chunk_d[:shift]
            chunk_l <<= shift
            chunk_d <<= shift
            chunk_l[-shift:], chunk_d[-shift:] = addition_l, addition_d

            # Final permutation
            new_key = self._permutation(chunk_l + chunk_d, DES_PC_2_TABLE)
            keys.append(new_key)

        return keys

    @staticmethod
    def _permutation(key: bitarray, table: tuple):
        return bitarray(key[i - 1] for i in table)

    def _transform(self, block: bitarray, mode: str = "encrypt"):
        block = self._permutation(block, DES_IP_TABLE)
        chunk_l, chunk_r = block[:32], block[32:]

        match mode:
            case "encrypt":
                for i in range(16):
                    chunk_l, chunk_r = chunk_r, chunk_l ^ self._feistel(chunk_r, self.keys[i])

            case "decrypt":
                for i in range(15, -1, -1):
                    chunk_r, chunk_l = chunk_l, chunk_r ^ self._feistel(chunk_l, self.keys[i])

            case _:
                raise DESError(f"Invalid processing mode! -> {mode}")

        return self._permutation(chunk_l + chunk_r, DES_IP_INV_TABLE)

    def _feistel(self, chunk: bitarray, key: bitarray):
        chunk = self._permutation(chunk, DES_E_TABLE)
        chunk ^= key

        new_chunk = bitarray()
        for k, pos in enumerate(range(0, 48, 6)):
            b = chunk[pos:pos + 6]
            i = ba2int(b[::5])
            j = ba2int(b[1:5])
            b = int2ba(DES_S_TABLE[k][i][j], length=4)
            new_chunk += b

        return self._permutation(new_chunk, DES_P_TABLE)

    def _ECB(self, data: bitarray, mode: str = "encrypt"):
        processed_data = bitarray()

        for pos in range(0, len(data), 64):
            block = data[pos:pos + 64]
            processed_block = self._transform(block, mode)
            processed_data += processed_block

        return processed_data

    def _CBC(self, data: bitarray, mode: str = "encrypt"):
        processed_data = bitarray()
        vector = self.iv

        for pos in range(0, len(data), 64):
            block = data[pos:pos + 64]

            match mode:
                case "encrypt":
                    processed_block = self._transform(block ^ vector, "encrypt")
                    vector = processed_block

                case "decrypt":
                    processed_block = self._transform(block, "decrypt") ^ vector
                    vector = block

                case _:
                    raise DESError(f"Invalid processing mode! -> {mode}")

            processed_data += processed_block

        return processed_data

    def _CFB(self, data: bitarray, mode: str = "encrypt"):
        processed_data = bitarray()
        vector = self.iv

        for pos in range(0, len(data), 64):
            block = data[pos:pos + 64]

            match mode:
                case "encrypt":
                    processed_block = self._transform(vector, "encrypt") ^ block
                    vector = processed_block

                case "decrypt":
                    processed_block = self._transform(vector, "encrypt") ^ block
                    vector = block

                case _:
                    raise DESError(f"Invalid processing mode! -> {mode}")

            processed_data += processed_block

        return processed_data

    def _OFB(self, data: bitarray, mode: str = "encrypt"):
        processed_data = bitarray()
        vector = self.iv

        for pos in range(0, len(data), 64):
            block = data[pos:pos + 64]

            match mode:
                case "encrypt":
                    vector = self._transform(vector, "encrypt")
                    processed_block = vector ^ block

                case "decrypt":
                    vector = self._transform(vector, "encrypt")
                    processed_block = vector ^ block

                case _:
                    raise DESError(f"Invalid processing mode! -> {mode}")

            processed_data += processed_block

        return processed_data

    def _data_processing(self, data: bytes or str, mode: str = "encrypt"):
        data_bits = bitarray()

        match mode, data:
            case "encrypt", str():
                data_bits.frombytes(data.encode("utf-8"))

            case "decrypt", str():
                data_bits = hex2ba(data)

            case _, bytes():
                data_bits.frombytes(data)

            case _:
                raise DESError(f"Invalid processing mode! -> {mode}")

        if mode == "encrypt" and (k := len(data_bits) % 64) != 0:
            data_bits += bitarray("0" * (64 - k))

        processed_data = self._mode(data_bits, mode)

        match mode, data:
            case "encrypt", str():
                return ba2hex(processed_data)

            case "decrypt", str():
                return processed_data.tobytes().decode("utf-8")

            case _, bytes():
                return processed_data.tobytes()

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
