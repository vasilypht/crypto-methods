import string
from typing import Final

ENGLISH_LETTERS: Final = string.ascii_lowercase
RUSSIAN_LETTERS: Final = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def encrypt(text: str) -> str:
    letters_list: list[str] = list(text)
    for i in range(len(text)):
        letter = letters_list[i].lower()

        if letter in ENGLISH_LETTERS:
            pos = ENGLISH_LETTERS.index(letter)
            letter = ENGLISH_LETTERS[len(ENGLISH_LETTERS) - pos - 1]
        elif letter in RUSSIAN_LETTERS:
            pos = RUSSIAN_LETTERS.index(letter)
            letter = RUSSIAN_LETTERS[len(RUSSIAN_LETTERS) - pos - 1]
        else:
            continue

        if letters_list[i].isupper():
            letter = letter.upper()

        letters_list[i] = letter
    return ''.join(letters_list)


def make(text: str) -> str:
    return encrypt(text)
