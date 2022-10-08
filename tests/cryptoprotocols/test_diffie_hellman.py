import pytest

from app.crypto.protocols import DiffieHellman


@pytest.mark.parametrize("key_len", [1024, 512, 256, 128, 64])
class TestDiffieHellman:

    def test_df(self, key_len):
        DH = DiffieHellman
        shared_keys = DH.gen_shared_keys(key_len)
        user_1 = DH(*DH.gen_keys(shared_keys), shared_keys)
        user_2 = DH(*DH.gen_keys(shared_keys), shared_keys)

        user_1.create_shared_private_key(user_2.public_key)
        user_2.create_shared_private_key(user_1.public_key)

        assert user_1.shared_private_key.k == user_2.shared_private_key.k
