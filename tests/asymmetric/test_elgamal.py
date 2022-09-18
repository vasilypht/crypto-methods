import pytest

from app.crypto.asymmetric import Elgamal
from app.crypto.common import EncProc


@pytest.mark.parametrize("data,key_length", [
    (63456234, 512),
    (534897538979, 612),
    (542870924709, 712)
])
class TestElgamal:

    def test_make(self, data, key_length):
        private_key, public_key = Elgamal.gen_keys(key_length)
        cipher = Elgamal(private_key, public_key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert data == decrypted_data

    def test_encrypt_decrypt(self, data, key_length):
        private_key, public_key = Elgamal.gen_keys(key_length)
        cipher = Elgamal(private_key, public_key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert data == decrypted_data
