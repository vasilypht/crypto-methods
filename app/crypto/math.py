
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


def ext_gcd(a, b):
    s0, s1 = 1, 0
    t0, t1 = 0, 1

    swap_flag = False
    if a < b:
        a, b = b, a
        swap_flag = True

    while b:
        q = a // b
        a, b = b, a % b
        s0, s1 = s1, s0 - s1 * q
        t0, t1 = t1, t0 - t1 * q

    if swap_flag:
        answer = (a, t0, s0)
    else:
        answer = (a, s0, t0)

    return answer
