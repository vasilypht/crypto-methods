import string
from typing import Final

ENG_LETTERS: Final = string.ascii_lowercase
RUS_LETTERS: Final = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def encrypt(text: str, shift: int = 1):
    encrypted_text = ""

    for char in text:
        char_lower = char.lower()

        for alphabet in (ENG_LETTERS, RUS_LETTERS):
            if char_lower not in alphabet:
                continue

            i = alphabet.index(char_lower)
            new_i = (i + shift) % len(alphabet)

            char_lower = alphabet[new_i]
            break

        if char.isupper():
            char = char_lower.upper()
        else:
            char = char_lower

        encrypted_text += char

    return encrypted_text


def decrypt(text: str, shift: int = 1):
    decrypted_text = ""

    for char in text:
        char_lower = char.lower()

        for alphabet in (ENG_LETTERS, RUS_LETTERS):
            if char_lower not in alphabet:
                continue

            i = alphabet.index(char_lower)
            new_i = (i - shift) % len(alphabet)

            char_lower = alphabet[new_i]
            break

        if char.isupper():
            char = char_lower.upper()
        else:
            char = char_lower

        decrypted_text += char

    return decrypted_text


def make(text: str, shift: int = 1, processing_type: str = "Encrypt"):
    match processing_type:
        case "Encrypt":
            return encrypt(text, shift)

        case "Decrypt":
            return decrypt(text, shift)

        case _:
            raise Exception("Invalid processing type!")
