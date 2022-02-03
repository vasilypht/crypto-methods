import pytest

from src.methods.symmetric import atbash


@pytest.mark.parametrize("text, encrypted_text",
                         [
                             ("Привет Мир!", "Поцэъм Тцо!"),
                             ("Hello, World!", "Svool, Dliow!"),
                             ("Hello, Мир! 123 ???[_]", "Svool, Тцо! 123 ???[_]")
                         ])
def test_encrypt(text, encrypted_text):
    assert atbash.encrypt(text) == encrypted_text


@pytest.mark.parametrize("encrypted_text, decrypted_text",
                         [
                             ("Поцэъм Тцо!", "Привет Мир!"),
                             ("Svool, Dliow!", "Hello, World!"),
                             ("Svool, Тцо! 123 ???[_]", "Hello, Мир! 123 ???[_]")
                         ])
def test_decrypt(encrypted_text, decrypted_text):
    decrypted = atbash.encrypt
    assert decrypted(encrypted_text) == decrypted_text

