# This module contains the implementation of the index of coincidence analysis method.
from collections import Counter
from itertools import zip_longest

from app.crypto.const import (
    ALPHABET_TABLE,
    IC_TABLE
)
from app.crypto.common import Languages


class IndexOfCoincidence:
    def __init__(self, text: str, max_len: int = 20, delta: float = 0.001, lang: Languages = Languages.ENGLISH) -> None:
        """
        The cryptanalysis method is based on calculating the probability that two random text elements will match.

        Args:
            text: text for analysis.
            max_len: maximum key length.
            delta: the value of the error when compared with the tabular values of the coincidence indices.
            lang: the language in which the analysis is to be carried out (Languages enum).
        """
        self.text = text.lower()
        self.max_len = max_len
        self.delta = delta

        if lang not in ALPHABET_TABLE.keys():
            raise ValueError(f"The selected language must be from the list -> {ALPHABET_TABLE.keys()}.")

        if lang not in IC_TABLE.keys():
            raise ValueError(f"The selected language must be from the list -> {IC_TABLE.keys()}.")

        self.alphabet = ALPHABET_TABLE.get(lang)
        self.threshold = IC_TABLE.get(lang)

        if not set(self.text).issubset(self.alphabet):
            raise ValueError("The text you entered contains invalid characters.")

    def ic(self, counter: Counter or dict) -> float:
        """Method for calculating the index of coincidences by formula."""
        numerator = sum(counter[letter] * (counter[letter] - 1) for letter in self.alphabet)
        size = sum(counter.values())
        denominator = size * (size - 1)
        if denominator == 0:
            denominator = 0.0000001
        return numerator / denominator

    def mic(self, counter_1: Counter or dict, counter_2: Counter or dict):
        """Method for calculating the mutual index of coincidences by the formula."""
        numerator = sum(counter_1[letter] * counter_2[letter] for letter in self.alphabet)
        size_1 = sum(counter_1.values())
        size_2 = sum(counter_2.values())
        denominator = size_1 * size_2
        return numerator / denominator

    def _shift_text(self, text: str, shift: int) -> str:
        """Method for shifting text alphabetically."""
        shifted_alphabet = ''.join(self.alphabet[(i + shift) % len(self.alphabet)] for i in range(len(self.alphabet)))
        translate_map = str.maketrans(self.alphabet, shifted_alphabet)
        return text.translate(translate_map)

    def _find_column_shifts(self, columns: tuple):
        """Method for finding possible offsets for each letter of a key. Accepts a tuple of strings where
        the letters in each string are likely to have the same offset from the key letter."""
        shifts = [0]

        for i in range(1, len(columns)):
            for shift in range(len(self.alphabet)):
                shifted_column = self._shift_text(columns[i], shift)
                mic = self.mic(Counter(columns[0]), Counter(shifted_column))
                if mic > self.threshold - self.delta:
                    shifts.append(shift)
                    break

        return shifts

    def find_possible_key_length(self):
        """Method for finding the possible key length."""
        for k in range(1, self.max_len + 1):
            groups = tuple(self.text[i:i + k] for i in range(0, len(self.text), k))
            ics = [self.ic(Counter("".join(column))) for column in zip_longest(*groups, fillvalue="")]
            ic_mean = sum(ics) / len(ics)
            if ic_mean > self.threshold - self.delta:
                return k

        raise ValueError("The key could not be found, try increasing "
                         "the error value or increasing the maximum key size.")

    def find_possible_keys(self, key_length: int) -> tuple[str]:
        """Method for finding possible key values."""
        groups = tuple(self.text[i:i + key_length] for i in range(0, len(self.text), key_length))
        columns = tuple("".join(column) for column in zip_longest(*groups, fillvalue=""))
        shifts = self._find_column_shifts(columns)

        if len(shifts) != len(columns):
            raise ValueError("Unable to find all shifts, try increasing the error.")

        shifted_columns = [columns[0]]
        for i in range(1, len(columns)):
            shifted_column = self._shift_text(columns[0], -shifts[i])
            shifted_columns.append(shifted_column)

        unique_keys = set("".join(value) for value in zip_longest(*shifted_columns, fillvalue=""))
        return tuple(unique_keys)
