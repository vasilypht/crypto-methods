import pytest

from app.crypto.symmetric import Richelieu
from app.crypto.common import EncProc
from app.crypto.exceptions import RichelieuError


@pytest.mark.parametrize("data,key", [
    ("Шифрование используется для скрытия информации от неавторизованных пользователей при передаче или при хранении.",
     "(2,1,3)(4,2,1,3)(2,1)"),
    ("Шифрование используется для предотвращения изменения информации при передаче или хранении.",
     "(3,1,2)(3,2,1)"),
    ("In cryptography, encryption is the process of encoding information.",
     "(2,1)(3,4,1,2)")
])
class TestRichelieu:

    def test_make(self, data, key):
        cipher = Richelieu(key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, key):
        cipher = Richelieu(key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_not_text():
    with pytest.raises(RichelieuError):
        Richelieu("(3,1,2)(3,2,1)").make("")


def test_not_key():
    with pytest.raises(RichelieuError):
        Richelieu("")


def test_error_key():
    with pytest.raises(RichelieuError):
        Richelieu("(1, 2)")

    with pytest.raises(RichelieuError):
        Richelieu("(2,3)")

    with pytest.raises(RichelieuError):
        Richelieu("(1,2),(3,2)")

    with pytest.raises(RichelieuError):
        Richelieu("1,2")
