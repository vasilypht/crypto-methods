import pytest

from app.crypto.mathlib import (
    fpow, ext_gcd, modinv
)


@pytest.mark.parametrize("a,n,m,result", [
    (2, 10, None, 1024),
    (23, 11, None, 952_809_757_913_927),
    (32_478_632_476_878_923, 2_438_972_348_975_490_234,
     2_314_987_234_098_453_098, 971_146_085_712_256_735),
    (123, 0, None, 1)
])
def test_fpow(a, n, m, result):
    assert fpow(a, n, m) == result


@pytest.mark.parametrize("a,n,m", [
    ("1", 2, None),
    (2, "1", None),
    ("2", "1", None),
    (3, 5, "5"),
    (3, 5, 3.4)
])
def test_fpow_error_value(a, n, m):
    with pytest.raises(ValueError):
        fpow(a, n, m)


@pytest.mark.parametrize("a,b,d,x,y", [
    (134234, 1235364, 2, 135193, -14690),
    (3456, 123123125644, 4, -11792174360, 331),
    (23, 2356475682, 1, -717188251, 7)
])
def test_ext_gcd(a, b, d, x, y):
    assert ext_gcd(a, b) == (d, x, y)


@pytest.mark.parametrize("a,b", [
    (134234, "1235364"),
    ("3456", 123123125644),
    ("23", "2356475682")
])
def test_ext_gcd_error_value(a, b):
    with pytest.raises(ValueError):
        ext_gcd(a, b)


@pytest.mark.parametrize("a,m,res", [
    (23, 2356475682, 1639287431),
    (534346, 123543265457, 71772619899),
    (4562323, 234234234234234234, 151806922968017875)
])
def test_modinv(a, m, res):
    assert modinv(a, m) == res


@pytest.mark.parametrize("a,m", [
    (134234, 1235364),
    (3456, 123123125644),
])
def test_modinv_error_value(a, m):
    with pytest.raises(ValueError):
        modinv(a, m)

