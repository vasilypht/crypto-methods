from dataclasses import dataclass
from secrets import SystemRandom

from app.crypto.mathlib import (ext_gcd, fpow)


class ElgamalDS:

    @dataclass
    class PublicKey:
        y: int
        g: int
        p: int

    @dataclass
    class PrivateKey:
        x: int
        g: int
        p: int

    @dataclass
    class Signature:
        r: int
        s: int

    def __init__(
            self,
            pr_key: PrivateKey = None,
            pb_key: PublicKey = None
    ):
        self._pr_key = pr_key
        self._pb_key = pb_key
        self._sysrand = SystemRandom()

    def sign(self, hvalue: str) -> Signature:
        if self._pr_key is None:
            raise ValueError("To sign a message, you must specify a private key!")

        ivalue = int(hvalue, 16)

        while True:
            k = self._sysrand.randrange(2, self._pr_key.p - 1)
            egcd_k = ext_gcd(k, self._pr_key.p - 1)

            if egcd_k.gcd == 1:
                break

        r = fpow(self._pr_key.g, k, self._pr_key.p)
        s = (ivalue - self._pr_key.x*r) * egcd_k.x % (self._pr_key.p - 1)

        return ElgamalDS.Signature(r, s)

    def verify(self, sign: Signature, hvalue: str) -> bool:
        if self._pb_key is None:
            raise ValueError("To verify a message, you must specify a public key!")

        ivalue = int(hvalue, 16)

        yr = fpow(self._pb_key.y, sign.r, self._pb_key.p)
        rs = fpow(sign.r, sign.s, self._pb_key.p)
        return yr*rs % self._pb_key.p == fpow(self._pb_key.g, ivalue, self._pb_key.p)
