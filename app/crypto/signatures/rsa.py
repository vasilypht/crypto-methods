from typing import Optional
from dataclasses import dataclass

from app.crypto.mathlib import fpow


class RSADS:
    @dataclass
    class PublicKey:
        e: int
        n: int

    @dataclass
    class PrivateKey:
        d: int
        n: int

    def __init__(
            self,
            pr_key: Optional[PrivateKey] = None,
            pb_key: Optional[PublicKey] = None,
    ) -> None:
        self._pr_key = pr_key
        self._pb_key = pb_key

    def sign(self, hvalue: str) -> str:
        if self._pr_key is None:
            raise ValueError("To sign a message, you must specify a private key!")

        ivalue = int(hvalue, 16)
        sign = fpow(ivalue, self._pr_key.d, self._pr_key.n)

        return hex(sign)[2:]

    def verify(self, sign: str, hvalue: str) -> bool:
        if self._pb_key is None:
            raise ValueError("To verify a message, you must specify a public key!")

        sign_ivalue = int(sign, 16)
        ivalue = int(hvalue, 16)

        return fpow(sign_ivalue, self._pb_key.e, self._pb_key.n) == ivalue
