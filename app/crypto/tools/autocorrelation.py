from itertools import zip_longest
from collections import Counter

from scipy.stats import chisquare
import numpy as np

from app.crypto.const import (
    ALPHABET_TABLE,
    IC_TABLE,
    FREQ_TABLES
)
from app.crypto.common import (
    Languages,
    TextStyle
)


class AutocorrError(Exception):
    pass


class Autocorrelation:
    def __init__(self, text, delta: float = 0.001, max_len: int = 20, lang: Languages = Languages.ENGLISH):
        self.text = text.lower()
        self.delta = delta
        self.max_len = max_len

        if lang not in ALPHABET_TABLE.keys():
            raise AutocorrError(f"The selected language must be from the list -> {ALPHABET_TABLE.keys()}")

        if lang not in FREQ_TABLES.keys():
            raise AutocorrError(f"The selected language must be from the list -> {FREQ_TABLES.keys()}")

        if lang not in IC_TABLE.keys():
            raise AutocorrError(f"The selected language must be from the list -> {IC_TABLE.keys()}")

        self.lang = lang
        self.alphabet = ALPHABET_TABLE.get(lang)
        self.threshold = IC_TABLE.get(lang)
        freq_table = FREQ_TABLES.get(lang).get(TextStyle.COMMON)
        freq_table_norm = self.freq_normalize(freq_table)
        self.freq_table = list(freq_table_norm.values())

        if not set(self.text).issubset(self.alphabet):
            raise AutocorrError("The text you entered contains invalid characters.")

    def find_possible_key_length(self):
        for t in range(1, min((len(self.text), self.max_len))):
            n = sum(1 for i in range(len(self.text) - t) if self.text[i] == self.text[i + t])
            autocorr_coff = n / (len(self.text) - t)
            if autocorr_coff > self.threshold - self.delta:
                return t

        raise AutocorrError("The key could not be found, try increasing "
                            "the error value or increasing the maximum key size.")

    @staticmethod
    def freq_normalize(counter: Counter or dict):
        return {key: value/sum(counter.values())*100 for key, value in counter.items()}

    def find_possible_key(self, key_len: int):
        groups = tuple(self.text[i:i + key_len] for i in range(0, len(self.text), key_len))
        columns = tuple("".join(column) for column in zip_longest(*groups, fillvalue=""))

        keys = []
        for column in columns:
            chi2_stats = []
            column_counter = dict.fromkeys(self.alphabet, 0.0000001)
            column_counter.update(Counter(column))
            column_freqs = list(column_counter.values())

            column_freqs = list(map(lambda x: x / sum(column_freqs) * 100, column_freqs))
            for i in range(len(self.alphabet)):
                shifted_column_freqs = column_freqs[i:] + column_freqs[:i]
                chi2_stats.append(chisquare(shifted_column_freqs, self.freq_table).statistic)

            keys.append(np.argmin(chi2_stats))
        return "".join(map(lambda x: self.alphabet[x], keys))
