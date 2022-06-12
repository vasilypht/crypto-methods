from random import randint

from ..const import (
    POLYBIUS_SQUARE_RU,
    POLYBIUS_SQUARE_EN,
    RUS_LCASE,
    ENG_LCASE
)
from ..utils import (
    get_letters_alphabetically
)


SQUARES = (
    POLYBIUS_SQUARE_EN,
    POLYBIUS_SQUARE_RU
)


class PolybiusSquareError(Exception):
    pass


class PolybiusSquare:
    def __init__(self, shift: int = 0, method: str = "method 1"):
        self.shift = shift

        if method not in ("method 1", "method 2"):
            raise PolybiusSquareError(f"Invalid method type! -> {method}")
        self.method = method

    @staticmethod
    def find_indices_in_square(letter: str, square: dict) -> tuple[int, int] or None:
        """The function of finding the index of an element in a given square.

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
        """Function to determine which square a letter belongs to.

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

    def _method_1(self, text: str, mode: str = "encrypt") -> str:
        """Polybius Square. Method 1. Function for encryption and decryption.

        Args:
            text: text to encrypt or decrypt.
            mode: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise PolybiusSquareError("Input text is empty!")

        text_list: list[str] = list(text)

        for i in range(len(text)):
            letter = text_list[i]

            if (square := self.get_square_by_letter(letter, SQUARES)) is None:
                continue

            letter_i, letter_j = self.find_indices_in_square(letter, square)

            match mode:
                case "encrypt":
                    if letter_j == 5:
                        letter_j = 1
                    else:
                        letter_j += 1

                case "decrypt":
                    if letter_j == 1:
                        letter_j = 5
                    else:
                        letter_j -= 1

                case _:
                    raise PolybiusSquareError(f"Invalid processing type! -> {mode}")

            new_letters = square.get((letter_i, letter_j))
            new_letter = new_letters[randint(0, 1)] if len(new_letters) == 2 else new_letters[0]

            if letter.islower():
                new_letter = new_letter.lower()

            text_list[i] = new_letter

        return "".join(text_list)

    def _method_2(self, text: str, mode: str = "encrypt") -> str:
        """Polybius Square. Method 2. Function for encryption and decryption.

        Args:
            text: text to encrypt or decrypt.
            mode: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise PolybiusSquareError("Input text is empty!")

        letters, indices = get_letters_alphabetically(text, ENG_LCASE + RUS_LCASE)

        indices_i = []
        indices_j = []
        for letter in letters:
            square = self.get_square_by_letter(letter, SQUARES)
            i, j = self.find_indices_in_square(letter, square)
            indices_i.append(i)
            indices_j.append(j)

        self.shift %= len(indices_i) + len(indices_j)

        match mode:
            case "encrypt":
                indices_ij = indices_i + indices_j
                indices_ij = indices_ij[self.shift::] + indices_ij[:self.shift:]
                new_indices = [(indices_ij[i], indices_ij[i + 1]) for i in range(0, len(indices_ij), 2)]

            case "decrypt":
                indices_ij = [index for pair in zip(indices_i, indices_j) for index in pair]
                indices_ij = indices_ij[len(indices_ij) - self.shift:] + indices_ij[:len(indices_ij) - self.shift:]
                k = len(indices_ij) // 2
                new_indices = list(zip(indices_ij[:k:], indices_ij[k::]))

            case _:
                raise PolybiusSquareError(f"Invalid processing type! -> {mode}")

        text_list: list[str] = list(text)

        for letter_index, (new_i, new_j) in zip(indices, new_indices):
            square = self.get_square_by_letter(text[letter_index], SQUARES)

            values = square.get((new_i, new_j))
            new_letter = values[randint(0, 1)] if len(values) == 2 else values[0]

            if text_list[letter_index].islower():
                new_letter = new_letter.lower()

            text_list[letter_index] = new_letter

        return "".join(text_list)

    def encrypt(self, text: str) -> str:
        """Polybius square cipher. Interface for calling encryption functions.

        Args:
            text: text to be encrypted.

        Returns:
            Encrypted string.
        """
        match self.method:
            case "method 1":
                return self._method_1(text, "encrypt")

            case "method 2":
                return self._method_2(text, "encrypt")

            case _:
                raise PolybiusSquareError(f"Invalid method type! -> {self.method}")

    def decrypt(self, text: str) -> str:
        """Polybius square cipher. Interface for calling decryption functions.

        Args:
            text: text to be decrypted.

        Returns:
            Decrypted string.
        """
        match self.method:
            case "method 1":
                return self._method_1(text, "decrypt")

            case "method 2":
                return self._method_2(text, "decrypt")

            case _:
                pass

    def make(self, text: str, mode: str = "encrypt") -> str:
        """Polybius square cipher. Interface for calling encryption/decryption functions.

        Args:
            text: text to be encrypted/decrypted.
            mode: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        match mode:
            case "encrypt":
                return self.encrypt(text)

            case "decrypt":
                return self.decrypt(text)

            case _:
                pass
