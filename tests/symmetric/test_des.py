import pytest

from app.crypto.symmetric import DES
from app.crypto.common import EncProc
from app.crypto.exceptions import DESError


@pytest.mark.parametrize("data,key,iv,enc_mode", [
    ("Hello, World! Hello,😱 World! Hello, World!", "8d380efc717b90", "f356687d1989b70b", DES.EncMode.CFB),
    ("Пример, Мир! Пример, 🥹 Мир! Пример, Мир!", "aa322b4e5ff2ab", "9b1cba443c565447", DES.EncMode.ECB),
    ("Привет, World! 🥶 Привет, World! Привет, World!", "4f1fbcd2a58a35", "ee9cf2f264955156", DES.EncMode.CBC),
    ("Hello, World! Hello,😱 World! Hello, World!", "8d380efc717b90", "f356687d1989b70b", DES.EncMode.OFB)
])
class TestDES:

    def test_make(self, data, key, iv, enc_mode):
        cipher = DES(key, iv, enc_mode)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert data == decrypted_data

    def test_encrypt_decrypt(self, data, key, iv, enc_mode):
        cipher = DES(key, iv, enc_mode)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert data == decrypted_data


def test_error_key_len():
    with pytest.raises(DESError):
        DES("8d380efc717b", "f356687d1989b70b", DES.EncMode.CFB)


def test_error_key():
    with pytest.raises(DESError):
        DES("8d380efc717bD-", "f356687d1989b70b", DES.EncMode.CFB)


def test_error_iv_len():
    with pytest.raises(DESError):
        DES("8d380efc717bad", "f356687d1989b70", DES.EncMode.CFB)


def test_error_iv():
    with pytest.raises(DESError):
        DES("8d380efc717bad", "f356687d1989b70=", DES.EncMode.CFB)


def test_empty_iv():
    with pytest.raises(DESError):
        DES("8d380efc717bad", enc_mode=DES.EncMode.CBC)

    with pytest.raises(DESError):
        DES("8d380efc717bad", enc_mode=DES.EncMode.OFB)

    with pytest.raises(DESError):
        DES("8d380efc717bad", enc_mode=DES.EncMode.CFB)

    try:
        DES("8d380efc717bad", enc_mode=DES.EncMode.ECB)

    except DESError:
        assert False
