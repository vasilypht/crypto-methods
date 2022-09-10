
def fpow(a, n, m=None) -> int:
    """Function for fast exponentiation modulo."""
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
