import pytest

from app.crypto.symmetric import PolybiusSquare
from app.crypto.common import EncProc


@pytest.mark.parametrize("data,shift,method", [
    ("Hel1o, World!", 2, PolybiusSquare.MethodMode.METHOD_1),
    ("блюдо богач вольт!", 10, PolybiusSquare.MethodMode.METHOD_2),
    ("что-то, World!", 11, PolybiusSquare.MethodMode.METHOD_2)
])
class TestPolybiusSquare:

    def test_make(self, data, shift, method):
        cipher = PolybiusSquare(shift, method)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, shift, method):
        cipher = PolybiusSquare(shift, method)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)
