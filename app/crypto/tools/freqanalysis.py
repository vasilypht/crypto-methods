# This module contains the implementation of the crypto frequency analysis method.
from collections import Counter

from app.crypto.exceptions import FreqAnalysisError
from app.crypto.utils import get_letters_alphabetically
from app.crypto.const import FREQ_TABLES
from app.crypto.common import (
    Languages,
    TextStyle
)


class FreqAnalysis:
    @staticmethod
    def get_freq_table(lang: Languages = Languages.ENGLISH, text_type: TextStyle = TextStyle.COMMON) -> dict:
        """Method for getting frequency table by text style and language."""
        return FREQ_TABLES.get(lang, {}).get(text_type, {})

    @staticmethod
    def analysis(text: str, freq_table: dict) -> dict:
        """A method for analyzing text by compiling a dictionary
        with alphabetical letter frequencies."""
        if not text:
            raise FreqAnalysisError("Input string is empty!")

        # We get the letters from the text that are in the alphabet.
        substr, _ = get_letters_alphabetically(text, freq_table.keys())

        if not substr:
            raise FreqAnalysisError("The input string does not have characters of the selected alphabet!")

        # We count the frequencies.
        counter_text = Counter(substr)

        # We form a dictionary, where the keys are the values of the alphabet.
        freq_text = dict.fromkeys(freq_table.keys(), 0)
        freq_text.update(counter_text)
        return freq_text

    @staticmethod
    def decipher(text: str, letter_match: dict) -> str:
        """Method for replacing text letters according to the letter ratio table."""
        if not text:
            raise FreqAnalysisError("Input string is empty!")

        # We create a translation table from lower and upper case letters.
        keys = ''.join(letter_match.keys())
        values = ''.join(letter_match.values())
        translate_map = str.maketrans(keys + keys.upper(), values + values.upper())

        return text.translate(translate_map)
