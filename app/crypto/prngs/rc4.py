# This module contains an implementation of a pseudo-random number generator
# based on the RC4 stream encryption algorithm
from ..exceptions import RC4Error


class RC4:
    def __init__(self, iv: str, n: int = 8):
        """
        Pseudorandom number generator based on the RC4 algorithm for streaming encryption.

        Args:
            iv: a string in hexadecimal format that initializes the value.
            n: size of generated number in bits.
        """
        if not iv:
            raise RC4Error("Initialization vector is empty!")

        try:
            self.iv = bytes.fromhex(iv)
        except ValueError:
            raise RC4Error("Error iv value! (must be hex)")

        self.n = n
        self.s = []
        self.i = 0
        self.j = 0
        self._ksa()

    def _ksa(self):
        """S-box initialization."""
        len_iv = len(self.iv)
        module = 2 ** self.n

        self.s = list(range(module))

        j = 0
        for i in range(256):
            j = (j + self.s[i] + self.iv[i % len_iv]) % module
            self.s[i], self.s[j] = self.s[j], self.s[i]

    def _prga(self):
        """Pseudo-random word generation K."""
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
