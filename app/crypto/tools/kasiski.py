# This module contains an implementation of the Kazisky method for cryptanalysis.
from math import gcd


class Kasiski:
    def __init__(self, text: str, seq_len: int = 3, threshold: int = 3, min_len: int = 3, max_len: int = 20):
        """
        Implementation of the method of cryptanalysis of polyalphabetic ciphers. Based on the
        fact that repeated parts of the plaintext encrypted with the same keyword result
        in identical ciphertext segments

        Args:
            text: text for analysis.
            seq_len: the length of the segment into which the text will be divided.
            threshold: the lower threshold for clipping rarely encountered segments in the text.
            min_len: minimum key length.
            max_len: minimum key length.
        """
        self.text = text.lower()
        self.seq_len = seq_len
        self.threshold = threshold
        self.min_len = min_len
        self.max_len = max_len

    @staticmethod
    def sequence_counter(text, seq_len: int = 3, threshold: int = 3):
        """A method for compiling a dictionary of segments and their frequency of occurrence in a text."""
        seq_counter = {}
        for i, letter in enumerate(text):
            seq = text[i:i + seq_len]

            # If the segment is not in the dictionary, then we initialize it in
            # the dictionary, otherwise we add its index.
            if seq in seq_counter.keys():
                seq_counter[seq].append(i)
            else:
                seq_counter[seq] = [i]

        # We take only those segments that met more than the specified threshold.
        filtered_seq_counter = {key: seq_counter[key] for key in
                                filter(lambda x: len(seq_counter[x]) >= threshold, seq_counter)}
        return filtered_seq_counter

    @staticmethod
    def get_distances(positions):
        """Method for calculating the distance between indices of the same segment."""
        return [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]

    def find_possible_key_lengths(self):
        """Method for calculating the distance between indices of the same segment."""
        possible_lengths = set()
        seq_counter = self.sequence_counter(self.text, self.seq_len, self.threshold)

        for positions in seq_counter.values():
            distances = self.get_distances(positions)
            possible_len = gcd(*distances)

            # The length of the key is the gcd of the distance between indices of the same
            # segment. Thus, it is likely that this value may be very large or very small in some cases.
            if self.min_len <= possible_len <= self.max_len:
                possible_lengths.add(possible_len)

        return sorted(possible_lengths)
