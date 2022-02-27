from .const import (
    ENG_LCASE,
    RUS_LCASE
)


def get_alphabet_by_letter(letter: str) -> tuple[str, str] or None:
    letter = letter.lower()

    for alphabet, lang in ((ENG_LCASE, "en"),
                           (RUS_LCASE, "ru")):
        if letter in alphabet:
            return alphabet, lang

    return None


def get_substr_from_alphabet(string: str, alphabet: str) -> tuple[str, list[int]]:
    indices = []

    letters = ""
    for i, letter in enumerate(string):
        if letter.lower() in alphabet:
            letters += letter
            indices.append(i)

    return letters, indices
