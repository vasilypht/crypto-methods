from math import gcd


class Kasiski:
    def __init__(self, text: str, seq_len: int = 3, threshold: int = 3, min_len: int = 3, max_len: int = 20):
        self.text = text.lower()
        self.seq_len = seq_len
        self.threshold = threshold
        self.min_len = min_len
        self.max_len = max_len

    @staticmethod
    def sequence_counter(text, seq_len: int = 3, threshold: int = 3):
        seq_counter = {}
        for i, letter in enumerate(text):
            seq = text[i:i + seq_len]
            if seq in seq_counter.keys():
                seq_counter[seq].append(i)
            else:
                seq_counter[seq] = [i]

        filtered_seq_counter = {key: seq_counter[key] for key in
                                filter(lambda x: len(seq_counter[x]) >= threshold, seq_counter)}
        return filtered_seq_counter

    @staticmethod
    def get_distances(positions):
        return [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]

    def find_possible_key_lengths(self):
        possible_lengths = set()
        seq_counter = self.sequence_counter(self.text, self.seq_len, self.threshold)

        for positions in seq_counter.values():
            distances = self.get_distances(positions)
            possible_len = gcd(*distances)
            if self.min_len <= possible_len <= self.max_len:
                possible_lengths.add(possible_len)
        return sorted(possible_lengths)
