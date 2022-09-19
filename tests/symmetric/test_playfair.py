import pytest

from app.crypto.symmetric import Playfair
from app.crypto.common import EncProc


@pytest.mark.parametrize("data,key", [
    ("Hel1o, World!", "wowomg"),
    ("Пример, Мир!", "ключ"),
    ("Привет, World!", "world")
])
class TestPlayfair:

    def test_make(self, data, key):
        cipher = Playfair(key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, key):
        cipher = Playfair(key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_not_key():
    with pytest.raises(ValueError):
        Playfair("")


def test_error_key():
    with pytest.raises(ValueError):
        Playfair("-123F")
