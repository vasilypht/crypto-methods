from .const import (
    ENG_LCASE,
    RUS_LCASE
)


def get_alphabet_by_letter(letter: str) -> str or None:
    letter = letter.lower()

    for alphabet in (ENG_LCASE, RUS_LCASE):
        if letter in alphabet:
            return alphabet

    return None


