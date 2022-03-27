from typing import Iterable


def get_alphabet_by_letter(
        letter: str,
        alphabets: tuple[tuple[str, str]]
) -> tuple[str, str] or None:
    letter = letter.lower()

    for alphabet, lang in alphabets:
        if letter in alphabet:
            return alphabet, lang

    return None


def get_substr_from_alphabet(
        string: str,
        alphabet: Iterable[str]) -> tuple[str, list[int]]:
    indices = []

    letters = ""
    for i, letter in enumerate(string):
        if letter.lower() in alphabet:
            letters += letter
            indices.append(i)

    return letters, indices
