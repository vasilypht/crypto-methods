import pytest

from app.crypto.symmetric import Vigenere
from app.crypto.common import EncProc
from app.crypto.exceptions import VigenereError


@pytest.mark.parametrize("data,key", [
    ("Шифрование используется для скрытия информации от неавторизованных пользователей при передаче или при хранении.",
     "КакойТоКлюч"),
    ("Шифрование используется для предотвращения изменения информации при передаче или хранении.",
     "SomeКлюч"),
    ("In cryptography, encryption is the process of encoding information.",
     "ШифрованиеEncrypt")
])
class TestVigenere:

    def test_make(self, data, key):
        cipher = Vigenere(key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, key):
        cipher = Vigenere(key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_not_text():
    with pytest.raises(VigenereError):
        Vigenere("КакойТоКлюч").make("")


def test_not_key():
    with pytest.raises(VigenereError):
        Vigenere("")


def test_error_key():
    with pytest.raises(VigenereError):
        Vigenere("123fasd")
