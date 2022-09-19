import pytest

from app.crypto.symmetric import Gronsfeld
from app.crypto.common import EncProc


@pytest.mark.parametrize("data,key", [
    ("Hello, World!", "23"),
    ("Пример, Мир!", "123432"),
    ("Привет, World!", "45623")
])
class TestGronsfeld:

    def test_make(self, data, key):
        cipher = Gronsfeld(key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert data == decrypted_data

    def test_encrypt_decrypt(self, data, key):
        cipher = Gronsfeld(key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert data == decrypted_data


def test_not_key():
    with pytest.raises(ValueError):
        Gronsfeld("")


def test_error_key():
    with pytest.raises(ValueError):
        Gronsfeld("-123F")
