from dataclasses import dataclass


class SHA1:
    @dataclass
    class Buffer:
        A: int
        B: int
        C: int
        D: int
        E: int

        @property
        def values(self):
            return self.A, self.B, self.C, self.D, self.E

    def __init__(self, data: str | bytes = b""):
        self._buffer = SHA1.Buffer(0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)
        self._data = b""
        self.update(data)

    def update(self, data: str | bytes = b""):
        match data:
            case str():
                self._data += data.encode("utf-8")

            case bytes():
                self._data += data

            case _:
                assert False

    def _collect(self) -> bytes:
        return b"".join(value.to_bytes(4, "big")
                        for value in self._buffer.values)

    @property
    def digest(self):
        b_data = self._data

        b_data = self._add_padding(b_data)
        self._drop_buffer()
        self._processing(b_data)
        return self._collect()

    @property
    def hexdigest(self):
        return self.digest.hex()

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

    def _drop_buffer(self):
        self._buffer = SHA1.Buffer(0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)

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
        _data += length.to_bytes(8, "big")
        return _data

    def _block_processing(self, block: bytes, **kwargs):
        read_block_size = kwargs.get("read_block_size")
        buffer_size = kwargs.get("buffer_size")

        if len(block) != read_block_size:
            block = self._add_padding(block, buffer_size * 8)

        self._processing(block)

    def _processing(self, _data: bytes):
        for i_block in range(0, len(_data), 64):
            block = _data[i_block:i_block + 64]
            parts = [int.from_bytes(block[i:i + 4], "big")
                     for i in range(0, 64, 4)]

            for i in range(16, 80):
                part = parts[i-3] ^ parts[i-8] ^ parts[i - 14] ^ parts[i-16]
                part = (part << 1 | part >> 31) & 0xFFFFFFFF
                parts.append(part)

            bf_a, bf_b, bf_c, bf_d, bf_e = self._buffer.values

            for i in range(80):
                if 0 <= i <= 19:
                    k = 0x5A827999
                    fn_value = (bf_b & bf_c) | (~bf_b & bf_d)

                elif 20 <= i <= 39:
                    k = 0x6ED9EBA1
                    fn_value = bf_b ^ bf_c ^ bf_d

                elif 40 <= i <= 59:
                    k = 0x8F1BBCDC
                    fn_value = (bf_b & bf_c) | (bf_b & bf_d) | (bf_c & bf_d)

                elif 60 <= i <= 79:
                    k = 0xCA62C1D6
                    fn_value = bf_b ^ bf_c ^ bf_d

                else:
                    assert False

                temp = (bf_a << 5 | bf_a >> 27) & 0xFFFFFFFF
                temp = (temp + fn_value) % 4_294_967_296
                temp = (temp + bf_e) % 4_294_967_296
                temp = (temp + parts[i]) % 4_294_967_296
                temp = (temp + k) % 4_294_967_296

                bf_e = bf_d
                bf_d = bf_c
                bf_c = (bf_b << 30 | bf_b >> 2) & 0xFFFFFFFF
                bf_b = bf_a
                bf_a = temp

            self._buffer.A = (self._buffer.A + bf_a) % 4_294_967_296
            self._buffer.B = (self._buffer.B + bf_b) % 4_294_967_296
            self._buffer.C = (self._buffer.C + bf_c) % 4_294_967_296
            self._buffer.D = (self._buffer.D + bf_d) % 4_294_967_296
            self._buffer.E = (self._buffer.E + bf_e) % 4_294_967_296


if __name__ == '__main__':
    sha1 = SHA1()
    sha1.hash_file("/Users/vasilyperekhrest/Downloads/PerekhrestVD_KI18-01_V12_Task3.pdf")

    print(sha1.hexdigest)
