from typing import NamedTuple


def fpow(a: int, n: int, m: int = None) -> int:
    """Function for fast exponentiation modulo."""
    if not (isinstance(a, int) and isinstance(n, int)):
        raise ValueError("Function arguments must be integers.")

    if m and not isinstance(m, int):
        raise ValueError("Function arguments must be integers.")

    result = 1

    while n > 0:
        if n & 1:
            result *= a
            if m:
                result %= m

        a **= 2
        if m:
            a %= m

        n >>= 1

    return result


class EEAResult(NamedTuple):
    """Result of the extended Euclidean algorithm"""
    gcd: int
    x: int
    y: int


def ext_gcd(a: int, b: int) -> EEAResult:
    """
    Extended Euclidean Algorithm.

    Returns a tuple (d, x, y) where a, b are the
    expansion coefficients: gcd = d = a*x + b*y
    """
    if not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError("Function arguments must be integers.")

    s0, s1 = 1, 0
    t0, t1 = 0, 1

    is_swapped = False
    if a < b:
        a, b = b, a
        is_swapped = True

    while b:
        q = a // b
        a, b = b, a % b
        s0, s1 = s1, s0 - s1 * q
        t0, t1 = t1, t0 - t1 * q

    if is_swapped:
        result = EEAResult(a, t0, s0)
    else:
        result = EEAResult(a, s0, t0)

    return result


def modinv(a: int, m: int) -> int:
    """
    Modular multiplicative inverse
    """
    g, x, y = ext_gcd(a, m)

    if g != 1:
        raise ValueError("Unable to find inverse element. The numbers "
                         "A and M must be relatively prime.")

    return x % m
