from math import sin
from dataclasses import dataclass


class MD5:
    @dataclass
    class Buffer:
        A: int
        B: int
        C: int
        D: int

        @property
        def values(self):
            return self.A, self.B, self.C, self.D

    def __init__(self, data: str | bytes = b""):
        self._buffer = MD5.Buffer(0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)
        self._table_t = [int(2 ** 32 * abs(sin(i + 1))) for i in range(64)]
        self._data = b""
        self.update(data)

    @property
    def digest(self) -> bytes:
        b_data = self._data

        b_data = self._add_padding(b_data)
        self._drop_buffer()
        self._processing(b_data)
        return self._collect()

    @property
    def hexdigest(self):
        return self.digest.hex()

    def _collect(self):
        return b"".join(value.to_bytes(4, "little")
                        for value in self._buffer.values)

    def update(self, data: str | bytes):
        match data:
            case str():
                self._data += data.encode("utf-8")

            case bytes():
                self._data += data

            case _:
                assert False

    def _block_processing(self, block: bytes, **kwargs):
        read_block_size = kwargs.get("read_block_size")
        buffer_size = kwargs.get("buffer_size")

        if len(block) != read_block_size:
            block = self._add_padding(block, buffer_size * 8)

        self._processing(block)

    def hash_file(self, file_path: str) -> bytes:
        with open(file_path, "rb") as ifile:
            ifile.seek(0, 2)
            ifile_size = ifile.tell()
            ifile.seek(0, 0)

            self._drop_buffer()

            while block := ifile.read(4096):
                if len(block) != 4096:
                    block = self._add_padding(block, ifile_size * 8)

                self._processing(block)

        return self._collect()

    @staticmethod
    def _add_padding(_data: bytes, length: int | None = None):
        if not length:
            length = len(_data) * 8

        last_block_length = len(_data) % 64
        if last_block_length >= 56:
            _data += b"\x80" + bytes(64 - 1 - last_block_length) + bytes(56)

        else:
            _data += b"\x80" + bytes(56 - 1 - last_block_length)

        length &= 0xFFFFFFFFFFFFFFFF
        length_le = int.from_bytes(reversed(length.to_bytes(8, "big")), "little")
        _data += length_le.to_bytes(8, "little")
        return _data

    def _drop_buffer(self):
        self._buffer = MD5.Buffer(0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)

    def _processing(self, b_data: bytes):
        for i_block in range(0, len(b_data), 64):
            block = b_data[i_block:i_block + 64]
            parts = [int.from_bytes(block[i:i + 4], "little") for i in range(0, 64, 4)]
            bf_a, bf_b, bf_c, bf_d = self._buffer.values

            for i in range(4 * 16):
                if 0 <= i <= 15:
                    k = i
                    s = (7, 12, 17, 22)
                    fn_value = (bf_b & bf_c) | (~bf_b & bf_d)

                elif 16 <= i <= 31:
                    k = (5 * i + 1) % 16
                    s = (5, 9, 14, 20)
                    fn_value = (bf_b & bf_d) | (~bf_d & bf_c)

                elif 32 <= i <= 47:
                    k = (3 * i + 5) % 16
                    s = (4, 11, 16, 23)
                    fn_value = bf_b ^ bf_c ^ bf_d

                elif 48 <= i <= 63:
                    k = 7 * i % 16
                    s = (6, 10, 15, 21)
                    fn_value = bf_c ^ (~bf_d | bf_b)

                else:
                    assert False

                temp = (bf_a + fn_value) % 4_294_967_296
                temp = (temp + parts[k]) % 4_294_967_296
                temp = (temp + self._table_t[i]) % 4_294_967_296
                temp = (temp << s[i % 4] | temp >> (32 - s[i % 4])) & 0xFFFFFFFF
                temp = (bf_b + temp) % 4_294_967_296

                bf_a = bf_d
                bf_d = bf_c
                bf_c = bf_b
                bf_b = temp

            self._buffer.A = (self._buffer.A + bf_a) % 4_294_967_296
            self._buffer.B = (self._buffer.B + bf_b) % 4_294_967_296
            self._buffer.C = (self._buffer.C + bf_c) % 4_294_967_296
            self._buffer.D = (self._buffer.D + bf_d) % 4_294_967_296


if __name__ == '__main__':
    md5 = MD5()
    md5.update("Hello, World!")
    print(md5.hexdigest)
