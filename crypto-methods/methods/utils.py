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


