import pytest

from app.crypto.symmetric import Atbash
from app.crypto.exceptions import AtbashError


@pytest.mark.parametrize("data", [
    "Hello, World!",
    "Пример, Мир!", "ключключ",
    "Привет, World!", "somekey"
])
class TestAtbash:

    def test_make(self, data):
        cipher = Atbash()

        encrypted_data = cipher.make(data)
        decrypted_data = cipher.make(encrypted_data)

        assert data == decrypted_data


def test_no_text():
    with pytest.raises(AtbashError):
        Atbash().make("")
