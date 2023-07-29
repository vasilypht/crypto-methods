from dataclasses import dataclass
from secrets import SystemRandom

from sympy import legendre_symbol, sqrt_mod

from app.crypto.mathlib import fpow, modinv


@dataclass
class ECParams:
    a: int
    b: int
    p: int
    q: int = -1

    def __eq__(self, other):
        return self.a == other.a and \
               self.b == other.b and \
               self.p == other.p and \
               self.q == other.q

    def __ne__(self, other):
        return not self == other


class ECPoint:
    def __init__(self, x: int, y: int, prm: ECParams, at_infinity: bool = False):
        self._x = x
        self._y = y
        self._ec_prm = prm
        self._at_infinity = at_infinity

    def inverse(self):
        y = -self._y % self._ec_prm.p
        return ECPoint(self._x, y, self._ec_prm, self._at_infinity)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def at_infinity(self):
        return self._at_infinity

    @property
    def params(self):
        return self._x, self._y, self._ec_prm, self._at_infinity

    @property
    def ec_params(self):
        return self._ec_prm

    def __neg__(self):
        return self.inverse()

    def __add__(self, other):
        if self.ec_params != other.ec_params:
            raise ValueError("Elliptic curves are different")

        if self.at_infinity:
            return ECPoint(*other.params)

        if other.at_infinity:
            return ECPoint(*self.params)

        if self.x == other.x and self.y != other.y:
            return ECPoint(0, 0, self._ec_prm, True)

        if self == other:
            m = (3 * self.x ** 2 + self.ec_params.a) * modinv(2 * self.y, self.ec_params.p) % self.ec_params.p
        else:
            delta_y = (self.y - other.y) % self._ec_prm.p
            delta_x = (self.x - other.x) % self._ec_prm.p
            m = delta_y * modinv(delta_x, self.ec_params.p) % self.ec_params.p

        xr = (m ** 2 - self.x - other.x) % self.ec_params.p
        yr = (-self.y + m * (self.x - xr)) % self.ec_params.p
        return ECPoint(xr, yr, self.ec_params, False)

    def __mul__(self, other):
        result = ECPoint(0, 0, self._ec_prm, True)
        value = ECPoint(*self.params)

        while other:
            if other & 1:
                result = result + value

            value = value + value
            other >>= 1

        return result

    def __eq__(self, other):
        return self._x == other.x and \
               self._y == other.y and \
               self._ec_prm == other.ec_params and \
               self._at_infinity == other.at_infinity

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"({self.x}, {self.y})"


class EllipticCurve:
    def __init__(self, prm: ECParams):
        if prm.p < 5 or (4 * fpow(prm.a, 3, prm.p) + 27 * fpow(prm.b, 2, prm.p)) % prm.p == 0:
            raise ValueError("Error!\n"
                             "Parameter p must be greater than 3.\n"
                             "Parameters a and b must satisfy the comparison 4a^3 + 27b^2 != 0 (mod p)\n")
        self._prm = prm
        self._sysrand = SystemRandom()

    def rand_point(self):
        while True:
            x = self._sysrand.randrange(1, self._prm.p)
            f = (fpow(x, 3, self._prm.p) + self._prm.a + x + self._prm.b) % self._prm.p

            if not (legendre_symbol(f, self._prm.p) != 1):
                break

        y = sqrt_mod(f, self._prm.p)
        return ECPoint(x, y, self._prm)

    def is_included_point(self, point: ECPoint):
        x = point.x
        y = point.y
        ec_prms = point.ec_params

        return y**2 % ec_prms.p == (x**3 + ec_prms.a*x + ec_prms.b) % ec_prms.p and ec_prms == self._prm
