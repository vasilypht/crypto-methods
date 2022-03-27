from collections import Counter

from src.crypto.utils import (
    get_substr_from_alphabet
)
from src.crypto.const import (
    FREQ_TABLES
)


class FreqAnalysisError(Exception):
    pass


def get_freq_table(lang: str = "english", text_type: str = "common") -> dict:
    return FREQ_TABLES.get(lang, {}).get(text_type, {})


def analysis(text: str, freq_table: dict) -> dict:
    if not text:
        raise FreqAnalysisError("Input string is empty!")

    substr, _ = get_substr_from_alphabet(text, freq_table.keys())

    if not substr:
        raise FreqAnalysisError("The input string does not have characters of the selected alphabet!")

    counter_text = Counter(substr)

    freq_text = dict.fromkeys(freq_table.keys(), 0)
    freq_text.update(counter_text)
    return freq_text


def decipher(text: str, freq_text: dict, freq_table: dict) -> str:
    if not text:
        raise FreqAnalysisError("Input string is empty!")

    freq_text_sorted_tuple = tuple(key for key, _ in sorted(freq_text.items(), key=lambda item: item[1]))
    freq_table_sorted_tuple = tuple(key for key, _ in sorted(freq_table.items(), key=lambda item: item[1]))

    test_list: list[str] = list(text)

    for i in range(len(text)):
        letter = test_list[i]
        if letter.lower() not in freq_table_sorted_tuple:
            continue

        new_letter_index = freq_text_sorted_tuple.index(letter.lower())
        new_letter = freq_table_sorted_tuple[new_letter_index]
        if letter.isupper():
            new_letter = new_letter.upper()

        test_list[i] = new_letter

    return "".join(test_list)
