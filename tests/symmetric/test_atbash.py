import pytest

from app.crypto.symmetric import Atbash


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
