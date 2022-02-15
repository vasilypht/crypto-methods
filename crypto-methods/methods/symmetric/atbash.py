from ..const import (
    ENG_LCASE,
    RUS_LCASE
)


def encrypt(text: str) -> str:
    letters_list: list[str] = list(text)
    for i in range(len(text)):
        letter = letters_list[i].lower()

        for alpha in (ENG_LCASE, RUS_LCASE):
            if letter not in alpha:
                continue

            pos = alpha.index(letter)
            letter = alpha[len(alpha) - pos - 1]

            if letters_list[i].isupper():
                letter = letter.upper()

            letters_list[i] = letter

    return ''.join(letters_list)


def make(text: str) -> str:
    return encrypt(text)
