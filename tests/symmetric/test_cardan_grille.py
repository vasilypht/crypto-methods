import pytest

from app.crypto.symmetric import CarganGrille
from app.crypto.common import EncProc
from app.crypto.exceptions import CarganGrilleError


@pytest.mark.parametrize("data,size_stencil", [
    ("Hello, World!", 2),
    ("Пример, Мир!", 3),
    ("Привет, World!", 4)
])
class TestCarganGrille:

    def test_make(self, data, size_stencil):
        stencil = CarganGrille.gen_stencil(size_stencil)
        cipher = CarganGrille(stencil, CarganGrille.EncMode.WITHOUT_TRASH)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

        cipher = CarganGrille(stencil, CarganGrille.EncMode.WITH_TRASH)

        encrypted_data = cipher.make(data, EncProc.ENCRYPT)
        decrypted_data = cipher.make(encrypted_data, EncProc.DECRYPT)

        assert decrypted_data.startswith(data)

    def test_encrypt_decrypt(self, data, size_stencil):
        stencil = CarganGrille.gen_stencil(size_stencil)
        cipher = CarganGrille(stencil, CarganGrille.EncMode.WITHOUT_TRASH)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)

        cipher = CarganGrille(stencil, CarganGrille.EncMode.WITH_TRASH)

        encrypted_data = cipher.encrypt(data)
        decrypted_data = cipher.decrypt(encrypted_data)

        assert decrypted_data.startswith(data)


def test_not_text():
    stencil = CarganGrille.gen_stencil(2)
    cipher = CarganGrille(stencil, CarganGrille.EncMode.WITHOUT_TRASH)

    with pytest.raises(CarganGrilleError):
        cipher.encrypt("")

    with pytest.raises(CarganGrilleError):
        cipher.decrypt("")


def test_correct_stencil():
    stencil = CarganGrille.gen_stencil(2)

    assert CarganGrille.check_correct_stencil(stencil)

    for i in range(4):
        for j in range(4):
            stencil[i, j].cond = True

    assert not CarganGrille.check_correct_stencil(stencil)

