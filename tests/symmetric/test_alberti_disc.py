import pytest

from app.crypto.symmetric import Alberti
from app.crypto.common import EncProc
from app.crypto.exceptions import AlbertiError


@pytest.mark.parametrize("data,key,step,shift", [
    ("Hello, World!", "somekey", 3, 10),
    ("Пример, Мир!", "ключключ", 12, 2),
    ("Привет, World!", "somekey", 2, 9)
])
class TestAlberti:

    def test_make(self, data, key, step, shift):
        cipher = Alberti(key, step, shift)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert data == decrypted_data

    def test_encrypt_decrypt(self, data, key, step, shift):
        cipher = Alberti(key, step, shift)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert data == decrypted_data


def test_not_key():
    with pytest.raises(AlbertiError):
        Alberti("", 3, 3)


def test_error_key():
    with pytest.raises(AlbertiError):
        Alberti("ЯR", 3, 3)


def test_error_step():
    with pytest.raises(AlbertiError):
        Alberti("aa", -1, 3)


def test_error_shift():
    with pytest.raises(AlbertiError):
        Alberti("aa", 1, -1)
