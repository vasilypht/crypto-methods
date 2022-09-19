import pytest

from app.crypto.symmetric import Vernam
from app.crypto.common import EncProc


@pytest.mark.parametrize("data", [
    "Шифрование используется для скрытия информации от неавторизованных пользователей при передаче или при хранении.",
    "Шифрование используется для предотвращения изменения информации при передаче или хранении.",
    "In cryptography, encryption is the process of encoding information."
])
class TestVernam:

    def test_make(self, data):
        key = Vernam.gen_key(len(data.encode("utf-8")))
        cipher = Vernam(key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data):
        key = Vernam.gen_key(len(data.encode("utf-8")))
        cipher = Vernam(key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_error_key():
    with pytest.raises(ValueError):
        Vernam("gggggg")


def test_not_key():
    with pytest.raises(ValueError):
        Vernam("")
