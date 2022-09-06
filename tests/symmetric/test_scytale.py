import pytest

from app.crypto.symmetric import Scytale
from app.crypto.common import EncProc
from app.crypto.exceptions import ScytaleError


@pytest.mark.parametrize("data,n", [
    ("Шифрование используется для скрытия информации от неавторизованных пользователей при передаче или при хранении.",
     3),
    ("Шифрование используется для предотвращения изменения информации при передаче или хранении.",
     4),
    ("In cryptography, encryption is the process of encoding information.",
     7)
])
class TestScytale:

    def test_make(self, data, n):
        cipher = Scytale(n)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, n):
        cipher = Scytale(n)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_error_n():
    with pytest.raises(ScytaleError):
        Scytale(0)

    with pytest.raises(ScytaleError):
        Scytale(-2)


def test_error_m():
    with pytest.raises(ScytaleError):
        Scytale(2, 0, False)

    with pytest.raises(ScytaleError):
        Scytale(2, -2, False)


def test_not_text():
    with pytest.raises(ScytaleError):
        Scytale(2).encrypt("")

    with pytest.raises(ScytaleError):
        Scytale(2).decrypt("")
