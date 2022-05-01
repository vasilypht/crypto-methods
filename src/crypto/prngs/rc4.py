class RC4Error(Exception):
    pass


class RC4:
    def __init__(self, iv: str, n: int = 8):
        if not iv:
            raise RC4Error("Initialization vector is empty!")

        try:
            self.iv = bytes.fromhex(iv)
        except ValueError:
            raise RC4Error("Error iv value! (must be hex)")

        self.n = n

        self._reset_state()

    def _reset_state(self):
        self.s = []
        self.i = 0
        self.j = 0

        self._ksa()

    def set_options(self, iv: str, n: int = 8):
        try:
            self.iv = bytes.fromhex(iv)
        except ValueError:
            raise RC4Error("Error iv value! (must be hex)")
        self.n = n

        self._reset_state()

    def _ksa(self):
        len_iv = len(self.iv)
        module = 2 ** self.n

        self.s = list(range(module))

        j = 0
        for i in range(256):
            j = (j + self.s[i] + self.iv[i % len_iv]) % module
            self.s[i], self.s[j] = self.s[j], self.s[i]

    def _prga(self):
        module = 2 ** self.n
        i, j = self.i, self.j

        i = (i + 1) % module
        j = (j + self.s[i]) % module

        self.i, self.j = i, j
        self.s[i], self.s[j] = self.s[j], self.s[i]

        t = (self.s[i] + self.s[j]) % module
        return self.s[t]

    def __iter__(self):
        return self

    def __next__(self):
        return self._prga()
