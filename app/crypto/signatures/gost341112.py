from typing import Optional
from dataclasses import dataclass
from secrets import SystemRandom

from app.crypto.const import CURVES
from app.crypto.elliptic_curve import (
    EllipticCurve,
    ECParams,
    ECPoint,
)
from app.crypto.mathlib import fpow, modinv


class GOST341112DS:
    @dataclass
    class PrivateKey:
        d: int

    @dataclass
    class PublicKey:
        x: int
        y: int

    def __init__(
            self,
            pr_key: Optional[PrivateKey] = None,
            pb_key: Optional[PublicKey] = None,
            curve: str = "gost256"
    ):
        curve_params = CURVES.get(curve)
        self._ec_prms = ECParams(
            curve_params.get("a"),
            curve_params.get("b"),
            curve_params.get("p"),
            curve_params.get("q"),
        )

        self._curve = EllipticCurve(self._ec_prms)

        match pb_key:
            case GOST341112DS.PublicKey(x, y):
                point = ECPoint(x, y, self._ec_prms)
                if self._curve.is_included_point(point):
                    self._pb_key = point
                else:
                    raise ValueError("")
            case _:
                self._pb_key = None

        match pr_key:
            case GOST341112DS.PrivateKey(d):
                self._pr_key = d
            case _:
                self._pr_key = None

        if fpow(2, 254) < self._ec_prms.q < fpow(2, 256):
            self._hash_num_bits = 256
            b = 31
        elif fpow(2, 508) < self._ec_prms.q < fpow(2, 512):
            self._hash_num_bits = 512
            b = 131
        else:
            raise ValueError("")

        for t in range(1, b+1):
            if fpow(self._ec_prms.p, t, self._ec_prms.q) != 1:
                continue
            else:
                raise ValueError("")

        if self._ec_prms.q * curve_params.get("n") == self._ec_prms.p:
            raise ValueError("")

        # inv
        _j1 = 4 * fpow(self._ec_prms.a, 3, self._ec_prms.p) % self._ec_prms.p
        _j2 = (4*fpow(self._ec_prms.a, 3, self._ec_prms.p) +
               27*fpow(self._ec_prms.b, 2, self._ec_prms.p)) % self._ec_prms.p
        j_e = (1728 * _j1 * modinv(_j2, self._ec_prms.p)) % self._ec_prms.p

        if j_e != 0 and j_e != 1728:
            pass
        else:
            raise ValueError("Error Value")

        self._pnt_p = ECPoint(*curve_params.get("base_point"), prm=self._ec_prms)

        self._sysrand = SystemRandom()

    @property
    def hash_dimension(self):
        return self._hash_num_bits

    def sign(self, hvalue: str) -> str:
        if not self._pr_key:
            raise ValueError("")

        ivalue = int(hvalue, 16)
        e = ivalue % self._ec_prms.q
        if e == 0:
            e = 1

        while True:
            k = self._sysrand.randrange(1, self._ec_prms.q)

            point_c = self._pnt_p * k
            r = point_c.x % self._ec_prms.q

            if r == 0:
                continue

            s = (r*self._pr_key + k*e) % self._ec_prms.q

            if s != 0:
                break

        vct_len = self._hash_num_bits // 8
        return r.to_bytes(vct_len, "big").hex() + s.to_bytes(vct_len, "big").hex()

    def verify(self, signature: str, hvalue: str) -> bool:
        if not self._pb_key:
            raise ValueError("")

        vct_len = self._hash_num_bits // 8 * 2
        r = int(signature[:vct_len], 16)
        s = int(signature[vct_len:], 16)

        ivalue = int(hvalue, 16)
        e = ivalue % self._ec_prms.q
        if e == 0:
            e = 1

        v = modinv(e, self._ec_prms.q)
        z1 = (s * v) % self._ec_prms.q
        z2 = (-r * v) % self._ec_prms.q

        point_c = self._pnt_p * z1 + self._pb_key * z2
        _r = point_c.x % self._ec_prms.q
        return _r == r

    @staticmethod
    def gen_keys(curve: str = "gost256"):
        prms = CURVES.get(curve, None)
        if not prms:
            raise ValueError("")

        ec_prms = ECParams(
            prms.get("a"),
            prms.get("b"),
            prms.get("p"),
            prms.get("q"),
        )
        point_p = ECPoint(*prms.get("base_point"), prm=ec_prms)

        sysrand = SystemRandom()
        d = sysrand.randrange(1, ec_prms.q)
        point_q = point_p * d
        return GOST341112DS.PrivateKey(d), GOST341112DS.PublicKey(point_q.x, point_q.y)
