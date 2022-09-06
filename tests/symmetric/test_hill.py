import pytest

from app.crypto.symmetric import Hill
from app.crypto.common import EncProc
from app.crypto.exceptions import HillError


@pytest.mark.parametrize("data,key,alphabet", [
    ("Hello, World!", "omgqweewq", "abcdefghijklmnopqrstuvwxyz! ,"),
    ("Пример, Мир!", "ключ ключ", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ,!"),
    ("Привет, World!", "пароль ух", "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя, !.-?")
])
class TestHill:

    def test_make(self, data, key, alphabet):
        cipher = Hill(key, alphabet)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, key, alphabet):
        cipher = Hill(key, alphabet)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_not_key():
    with pytest.raises(HillError):
        Hill("", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ,!")


def test_not_alphabet():
    with pytest.raises(HillError):
        Hill("asd", "")


def test_key_is_not_square():
    with pytest.raises(HillError):
        Hill("qwe", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ,!")


def test_key_is_not_subset_alphabet():
    with pytest.raises(HillError):
        Hill("абвгдеddd", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ,!")


def test_unique_alphabet_characters():
    with pytest.raises(HillError):
        Hill("абвг", "аабвгдеёжзийклмнопрстуфхцчшщъыьэюя ,!")


def test_not_text():
    with pytest.raises(HillError):
        Hill("omgqweewq", "abcdefghijklmnopqrstuvwxyz! ,").encrypt("")
