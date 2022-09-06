import pytest

from app.crypto.symmetric import Caesar
from app.crypto.common import EncProc
from app.crypto.exceptions import CaesarError


@pytest.mark.parametrize("data,shift", [
    ("Hello, World!", 10),
    ("Пример, Мир!", 2),
    ("Привет, World!", -9)
])
class TestCaesar:

    def test_make(self, data, shift):
        cipher = Caesar(shift)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert data == decrypted_data

    def test_encrypt_decrypt(self, data, shift):
        cipher = Caesar(shift)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert data == decrypted_data


def test_not_text():
    with pytest.raises(CaesarError):
        Caesar(2).make("")
