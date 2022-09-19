import pytest

from app.crypto.symmetric import XOR
from app.crypto.prngs import RC4
from app.crypto.common import EncProc


@pytest.mark.parametrize("data,iv,size_key", [
    ("Шифрование используется для скрытия информации от неавторизованных пользователей при передаче или при хранении.",
     "8d380efc717b90", 13),
    ("Шифрование используется для предотвращения изменения информации при передаче или хранении.",
     "4f1fbcd2a58a35", 7),
    ("In cryptography, encryption is the process of encoding information.",
     "8d380efc717b90", 21)
])
class TestXOR:

    def test_make(self, data, iv, size_key):
        rc4 = RC4(iv)
        xor_key = bytes(next(rc4) for _ in range(size_key)).hex()

        cipher = XOR(xor_key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, iv, size_key):
        rc4 = RC4(iv)
        xor_key = bytes(next(rc4) for _ in range(size_key)).hex()

        cipher = XOR(xor_key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_error_key():
    with pytest.raises(ValueError):
        XOR("ggggggg")


def test_not_key():
    with pytest.raises(ValueError):
        XOR("")
