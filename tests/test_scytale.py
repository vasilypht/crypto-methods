import pytest

from src.methods.symmetric import scytale


@pytest.mark.parametrize("text, encrypted_text, n, m",
                         [
                             ("Этошифрдревнейспарты", "Эфвптрнаодершрйтиесы", 4, 5),
                             ("НАС АТАКУЮТ", "НАУАТЮСАТ К", 3, 4),
                             ("THIS IS A SECRET MESSAGE", "TSCEH RSIAESS TA S GIEME", 4, 6),
                             ("123321 1111 212222", "12122211123 12 31 2", 5, 4)
                         ])
def test_encrypt(text: str, encrypted_text: str, n: int, m: int):
    assert scytale.encrypt(text, n, m) == encrypted_text


@pytest.mark.parametrize("encrypted_text, decrypted_text, n",
                         [
                             ("Эфвптрнаодершрйтиесы", "Этошифрдревнейспарты", 4),
                             ("НАУАТЮСАТ К", "НАС АТАКУЮТ", 3),
                             ("TSCEH RSIAESS TA S GIEME", "THIS IS A SECRET MESSAGE", 4),
                             ("12122211123 12 31 2", "123321 1111 212222", 5)
                         ])
def test_decrypt(encrypted_text, decrypted_text, n):
    assert scytale.decrypt(encrypted_text, n) == decrypted_text
