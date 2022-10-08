import pytest

from app.crypto.protocols import Shamir
from app.crypto.utils import gen_prime


@pytest.mark.parametrize("data,key_len", [
    (123432234234234, 1024),
    (423232323, 512),
    (1231231, 256),
    (432234, 128),
    (534345, 64)])
class TestShamir:

    def test_shamir(self, data, key_len):
        p = gen_prime(key_len)

        user_1 = Shamir(*Shamir.gen_keys(p))
        user_2 = Shamir(*Shamir.gen_keys(p))

        # User 1 -> User 2
        encrypted_data = user_1.encrypt(data)
        encrypted_data = user_2.encrypt(encrypted_data)

        decrypted_data = user_1.decrypt(encrypted_data)
        decrypted_data = user_2.decrypt(decrypted_data)

        assert data == decrypted_data
