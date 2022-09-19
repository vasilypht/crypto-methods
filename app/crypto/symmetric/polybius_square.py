# This module contains the implementation of the cipher "Polybius Square"
from random import randint
from enum import (
    Enum,
    auto
)

from ..const import (
    POLYBIUS_SQUARES_TABLE,
    ALPHABET_TABLE
)
from ..utils import get_letters_alphabetically
from ..common import EncProc


class PolybiusSquare:
    class MethodMode(Enum):
        """Method Modes for Polybius Square cipher."""
        METHOD_1 = auto()
        METHOD_2 = auto()

        @staticmethod
        def from_str(value: str):
            match value.lower():
                case "method 1":
                    return PolybiusSquare.MethodMode.METHOD_1

                case "method 2":
                    return PolybiusSquare.MethodMode.METHOD_2

                case _:
                    raise NotImplementedError()

    def __init__(self, shift: int = 0, method_mode: MethodMode = MethodMode.METHOD_1) -> None:
        """
        Implementation of the symmetric cipher "Polybius Square".

        Args:
            shift: the value by which the coordinates will be cyclically shifted.
                This parameter is used only in the second method.

            method_mode: encryption method. There are two kinds of methods for this
                cipher, and the second method can be used both with a zero shift
                and with a non-zero one.
        """
        if not isinstance(shift, int):
            raise TypeError("The key must be of type int!")

        self.shift = shift
        self.method_mode = method_mode

    @staticmethod
    def find_indices_in_square(letter: str, square: dict) -> tuple[int, int] or None:
        """
        Method for finding the index of an element in a given square.

        Args:
            letter: the letter whose index will be searched for.
            square: square to search.

        Returns:
            Element indices or None.
        """
        if not letter:
            return None

        for indices, letters in square.items():
            if letter.upper() in letters:
                return indices

    @staticmethod
    def get_square_by_letter(letter: str, squares: tuple) -> tuple[dict, dict, str] or None:
        """
        Method for determining which cell a letter belongs to.

        Args:
            letter: the letter for which you want to find the square.
            squares: squares to be searched.

        Returns:
            The desired square or None.
        """
        if not letter:
            return None

        for square in squares:
            if letter.upper() in [item for value in square.values() for item in value]:
                return square

    def _method_1(self, text: str, enc_proc: EncProc) -> str:
        """
        Method 1. Function for encryption and decryption.

        Args:
            text: the string to be encrypted or decrypted.
            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            return ""

        text_list: list[str] = list(text)

        for i in range(len(text)):
            letter = text_list[i]

            # We get a square by letter, if not, then we skip the iteration.
            if (square := self.get_square_by_letter(letter, POLYBIUS_SQUARES_TABLE.values())) is None:
                continue

            # We get the indices of the letter in the square.
            letter_i, letter_j = self.find_indices_in_square(letter, square)

            match enc_proc:
                case EncProc.ENCRYPT:
                    if letter_j == 5:
                        letter_j = 1
                    else:
                        letter_j += 1

                case EncProc.DECRYPT:
                    if letter_j == 1:
                        letter_j = 5
                    else:
                        letter_j -= 1

                case _:
                    raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")

            new_letters = square.get((letter_i, letter_j))
            # Some cells of the square have several letters, so we
            # choose one of the two with some probability.
            new_letter = new_letters[randint(0, 1)] if len(new_letters) == 2 else new_letters[0]

            if letter.islower():
                new_letter = new_letter.lower()

            text_list[i] = new_letter

        return "".join(text_list)

    def _method_2(self, text: str, enc_proc: EncProc) -> str:
        """Polybius Square. Method 2. Function for encryption and decryption.

        Args:
            text: text to encrypt or decrypt.
            enc_proc: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            return ""

        # We get only those letters and their indices in the source data that are in the squares.
        letters, indices = get_letters_alphabetically(text, ''.join(ALPHABET_TABLE.values()))

        indices_i = []
        indices_j = []
        for letter in letters:
            # We get a square by letter, if not, then we skip the iteration.
            square = self.get_square_by_letter(letter, POLYBIUS_SQUARES_TABLE.values())
            i, j = self.find_indices_in_square(letter, square)
            indices_i.append(i)
            indices_j.append(j)

        self.shift %= len(indices_i) + len(indices_j)

        match enc_proc:
            case EncProc.ENCRYPT:
                # Connecting superscripts and subscripts, and then shifting cyclically to the right.
                indices_ij = indices_i + indices_j
                indices_ij = indices_ij[self.shift::] + indices_ij[:self.shift:]

                # We form new pairs from the resulting sequence.
                new_indices = [(indices_ij[i], indices_ij[i + 1]) for i in range(0, len(indices_ij), 2)]

            case EncProc.DECRYPT:
                # We expand each pair of indices into one sequence.
                indices_ij = [index for pair in zip(indices_i, indices_j) for index in pair]
                # We make a reverse shift.
                indices_ij = indices_ij[len(indices_ij) - self.shift:] + indices_ij[:len(indices_ij) - self.shift:]

                # Forming new pairs of indices.
                k = len(indices_ij) // 2
                new_indices = list(zip(indices_ij[:k:], indices_ij[k::]))

            case _:
                raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")

        text_list: list[str] = list(text)

        # We place the changed letters back into the text.
        for letter_index, (new_i, new_j) in zip(indices, new_indices):
            square = self.get_square_by_letter(text[letter_index], POLYBIUS_SQUARES_TABLE.values())

            values = square.get((new_i, new_j))
            # Some cells of the square have several letters, so we
            # choose one of the two with some probability.
            new_letter = values[randint(0, 1)] if len(values) == 2 else values[0]

            if text_list[letter_index].islower():
                new_letter = new_letter.lower()

            text_list[letter_index] = new_letter

        return "".join(text_list)

    def encrypt(self, text: str) -> str:
        """
        Method for encrypting input data.

        Args:
            text: the string to be encrypted.

        Returns:
            Encrypted string.
        """
        match self.method_mode:
            case PolybiusSquare.MethodMode.METHOD_1:
                return self._method_1(text, EncProc.ENCRYPT)

            case PolybiusSquare.MethodMode.METHOD_2:
                return self._method_2(text, EncProc.ENCRYPT)

            case _:
                raise TypeError("Possible types: MethodMode.METHOD_1, MethodMode.METHOD_2.")

    def decrypt(self, text: str) -> str:
        """
        Method for decrypting input data.

        Args:
            text: the string to be decrypted.

        Returns:
            Decrypted string.
        """
        match self.method_mode:
            case PolybiusSquare.MethodMode.METHOD_1:
                return self._method_1(text, EncProc.DECRYPT)

            case PolybiusSquare.MethodMode.METHOD_2:
                return self._method_2(text, EncProc.DECRYPT)

            case _:
                raise TypeError("Possible types: MethodMode.METHOD_1, MethodMode.METHOD_2.")

    def make(self, text: str, enc_proc: EncProc = EncProc.ENCRYPT) -> str:
        """
        Method - interface for encrypting/decrypting input data.

        Args:
            text: the string to be encrypted or decrypted.

            enc_proc: parameter responsible for the process of data encryption (encryption and decryption).
                If the data object is of a different type, then an exception will be raised TypeError.

        Returns:
            Encrypted or decrypted string.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(text)

            case EncProc.DECRYPT:
                return self.decrypt(text)

            case _:
                TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")
