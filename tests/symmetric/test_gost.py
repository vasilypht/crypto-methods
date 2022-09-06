import pytest

from app.crypto.symmetric import GOST
from app.crypto.common import EncProc
from app.crypto.exceptions import GOSTError


@pytest.mark.parametrize("data,key,iv,enc_mode", [
    ("Hello, World! Hello,😱 World! Hello, World!",
     "0b8a3c2c7a407cc7d00d7a20dbba08be13d52de77bf76330dbc4aeaebcce6186",
     "f356687d1989b70b", GOST.EncMode.CFB),
    ("Пример, Мир! Пример, 🥹 Мир! Пример, Мир!",
     "c885b5ba69bca09c1c7e8b491506b3d753ed2604932077904c7449e1ab391a73",
     "9b1cba443c565447", GOST.EncMode.ECB),
    ("Привет, World! 🥶 Привет, World! Привет, World!",
     "62e0dcea9a0af290f17a2596bef4bd32244a23059fe77d481cc35063f6c62598",
     "ee9cf2f264955156", GOST.EncMode.CBC),
    ("Hello, World! Hello,😱 World! Hello, World!",
     "027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f29",
     "f356687d1989b70b", GOST.EncMode.OFB)
])
class TestGOST:

    def test_make(self, data, key, iv, enc_mode):
        cipher = GOST(key, iv, enc_mode)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert data == decrypted_data

    def test_encrypt_decrypt(self, data, key, iv, enc_mode):
        cipher = GOST(key, iv, enc_mode)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert data == decrypted_data


def test_error_key_len():
    with pytest.raises(GOSTError):
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f2",
             "f356687d1989b70b", GOST.EncMode.CFB)


def test_error_key():
    with pytest.raises(GOSTError):
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f2-",
             "f356687d1989b70b", GOST.EncMode.CFB)


def test_error_iv_len():
    with pytest.raises(GOSTError):
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f29",
             "f356687d1989b7", GOST.EncMode.CFB)


def test_error_iv():
    with pytest.raises(GOSTError):
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f29",
             "f356687d1989b70=", GOST.EncMode.CFB)


def test_empty_iv():
    with pytest.raises(GOSTError):
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f29",
             enc_mode=GOST.EncMode.CBC)

    with pytest.raises(GOSTError):
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f29",
             enc_mode=GOST.EncMode.OFB)

    with pytest.raises(GOSTError):
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f29",
             enc_mode=GOST.EncMode.CFB)

    try:
        GOST("027c9c9f8f44aaa186da7619ff012efd54401f2de3e4c4f930f4216f192d5f29",
             enc_mode=GOST.EncMode.ECB)

    except GOSTError:
        assert False
