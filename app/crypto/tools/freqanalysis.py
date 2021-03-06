from collections import Counter

from app.crypto.utils import (
    get_letters_alphabetically
)
from app.crypto.const import (
    FREQ_TABLES
)


class FreqAnalysisError(Exception):
    pass


def get_freq_table(lang: str = "english", text_type: str = "common") -> dict:
    return FREQ_TABLES.get(lang, {}).get(text_type, {})


def analysis(text: str, freq_table: dict) -> dict:
    if not text:
        raise FreqAnalysisError("Input string is empty!")

    substr, _ = get_letters_alphabetically(text, freq_table.keys())

    if not substr:
        raise FreqAnalysisError("The input string does not have characters of the selected alphabet!")

    counter_text = Counter(substr)

    freq_text = dict.fromkeys(freq_table.keys(), 0)
    freq_text.update(counter_text)
    return freq_text


def decipher(text: str, letter_match: dict) -> str:
    if not text:
        raise FreqAnalysisError("Input string is empty!")

    test_list: list[str] = list(text)

    for i in range(len(text)):
        letter = test_list[i]
        if letter.lower() not in letter_match.keys():
            continue

        new_letter = letter_match.get(letter.lower())
        if letter.isupper():
            new_letter = new_letter.upper()

        test_list[i] = new_letter

    return "".join(test_list)
