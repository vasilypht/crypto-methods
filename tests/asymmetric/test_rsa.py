import pytest

from app.crypto.asymmetric import RSA
from app.crypto.common import EncProc


@pytest.mark.parametrize("data,key_length", [
    (6345623451234, 1024),
    (534897543897234879, 2048),
    (542870924389712438709, 512)
])
class TestRSA:

    def test_make(self, data, key_length):
        private_key, public_key = RSA.gen_keys(key_length)
        cipher = RSA(private_key, public_key)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert data == decrypted_data

    def test_encrypt_decrypt(self, data, key_length):
        private_key, public_key = RSA.gen_keys(key_length)
        cipher = RSA(private_key, public_key)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert data == decrypted_data
