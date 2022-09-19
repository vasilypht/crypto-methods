# This module contains the implementation of the cipher "Grille Cardano"
from random import choice
from copy import deepcopy
from enum import (
    Enum,
    auto
)

import numpy as np

from ..common import EncProc


class Field:
    def __init__(self, value: int, cond: bool = False):
        """
        A wrapper over the stored value, a flag is additionally
        stored - whether the field is occupied or not.

        Args:
            value: the value to be wrapped.
            cond: whether this field is checked or not.
        """
        self.value = value
        self.cond = cond

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"Field({self.value}, {self.cond})"

    def __eq__(self, other):
        """Checking if the field is occupied or not. The value is multiplied
         by the flag (bool), resulting in zero or a value."""
        return self.value * self.cond == other


class CarganGrille:
    class EncMode(Enum):
        """Encryption Modes for Cipher Cardano Lattice."""
        WITH_TRASH = auto()
        WITHOUT_TRASH = auto()

        @staticmethod
        def from_str(value: str):
            match value.lower():
                case "with trash":
                    return CarganGrille.EncMode.WITH_TRASH

                case "without trash":
                    return CarganGrille.EncMode.WITHOUT_TRASH

                case _:
                    raise NotImplementedError()

    def __init__(self, stencil: np.ndarray, enc_mode: EncMode.WITHOUT_TRASH):
        """
        Implementation of the symmetric cipher "Cardano Lattice".

        Args:
            stencil: lattice over which encryption will occur.
            enc_mode: encryption mode, for this cipher there are several
                modes: with garbage, without garbage.
        """
        if not self.check_correct_stencil(stencil):
            raise ValueError("Wrong stencil!")

        self._stencil = stencil
        self._enc_mode = enc_mode

    @staticmethod
    def check_correct_stencil(square: np.array) -> bool:
        """
        A method for testing the validity of a stencil.

        Args:
            square: the generated lattice to be checked.

        Returns:
            True - if the stencil is correct, otherwise False.
        """
        s_1 = square
        s_2 = np.rot90(s_1, -1)
        s_3 = np.rot90(s_2, -1)
        s_4 = np.rot90(s_3, -1)

        n, m = square.shape
        if n != m or n < 2 or m < 2:
            return False

        # If nothing is selected
        if len(np.where(s_1 != 0)[0]) < 1:
            return False

        # Check for matching values
        for i in range(n):
            for j in range(n):
                if (s_1[i, j].cond, s_2[i, j].cond, s_3[i, j].cond, s_4[i, j].cond).count(True) > 1:
                    return False

        return True

    @staticmethod
    def gen_stencil(k: int) -> np.ndarray:
        """
        Method for generating a random stencil.

        Args:
            k: size of the side of the small square.

        Returns:
            Randomly generated stencil (numpy array).
        """
        if k < 1:
            raise ValueError("Error K value must be greater than 1!")

        # We generate a square according to the rule, and then we get
        # 3 copies, so that they can then be filled and glued.
        square_1 = [list(Field(j) for j in range(i*k + 1, i*k + k + 1)) for i in range(k)]
        square_2 = deepcopy(square_1)
        square_3 = deepcopy(square_1)
        square_4 = deepcopy(square_1)

        squares = (square_1, square_2, square_3, square_4)

        # We randomly select one square and mark the field by index as occupied.
        for i in range(k):
            for j in range(k):
                square = choice(squares)
                square[i][j].cond = True

        # We rotate each square depending on its position in one large square.
        square_2 = np.rot90(square_2, -1)
        square_3 = np.rot90(square_3, -2)
        square_4 = np.rot90(square_4, -3)

        # We connect all the squares into one.
        rect_1 = np.concatenate((square_1, square_2), axis=1)
        rect_2 = np.concatenate((square_4, square_3), axis=1)
        square = np.concatenate((rect_1, rect_2), axis=0, dtype=Field)

        return square

    def encrypt(self, text: str) -> str:
        """
        Method for encrypting input data.

        Args:
            text: the string to be encrypted.

        Returns:
            Encrypted string.
        """
        if not text:
            return ""

        stencil = self._stencil.copy()
        n, _ = stencil.shape

        # We are looking for all the cells in the stencil where there are holes.
        # Next, we take all these cells and sort them by values.
        indices_allow_values = np.where(stencil != 0)
        sorted_allow_values = sorted(stencil[indices_allow_values], key=lambda x: x.value)

        one_iter_len_text = len(sorted_allow_values) * 4

        # We divide the text into blocks.
        text_blocks = [text[i:i + one_iter_len_text] for i in range(0, len(text), one_iter_len_text)]

        encrypted_text = ""

        for text_block in text_blocks:
            square = np.empty((n, n), dtype=str)
            square.fill("")

            for i in range(0, len(text_block), len(sorted_allow_values)):
                substr = text_block[i:i+len(sorted_allow_values)]

                # We insert letters by sorted values, then rotate the square by
                # 90 degrees and repeat the encryption again.
                for char, value in zip(substr, sorted_allow_values):
                    indices_value = np.where(stencil == value)
                    square[indices_value] = char

                stencil = np.rot90(stencil, -1)

            # We fill in the empty fields of the lattice.
            indices = np.where(square == "")
            match self._enc_mode:
                case CarganGrille.EncMode.WITH_TRASH:
                    # Random letters of text.
                    rand_letters = [choice(text) for _ in range(len(indices[0]))]
                    square[indices] = rand_letters

                case CarganGrille.EncMode.WITHOUT_TRASH:
                    # Filling with spaces
                    square[indices] = " "

                case _:
                    raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")

            encrypted_text += "".join("".join(i) for i in square)

        return encrypted_text

    def decrypt(self, text: str) -> str:
        """
        Method for decrypting input data.

        Args:
            text: the string to be decrypted.

        Returns:
            Decrypted string.
        """
        if not text:
            return ""

        stencil = self._stencil.copy()
        n, _ = stencil.shape

        # We are looking for all the cells in the stencil where there are holes.
        # Next, we take all these cells and sort them by values.
        indices_allow_values = np.where(stencil != 0)
        sorted_allow_values = sorted(stencil[indices_allow_values], key=lambda x: x.value)

        # We divide the text into blocks.
        text_blocks = [text[i:i + n ** 2] for i in range(0, len(text), n ** 2)]
        text_blocks[-1] += " " * (n**2 - len(text_blocks[-1]))

        decrypted_text = ""

        for text_block in text_blocks:
            # We form a square from the block.
            square = np.array(list(text_block)).reshape((n, n))

            for _ in range(4):
                # By sorted values, we take letters from the formed square. By sorted values,
                # we take letters from the formed square. Then rotate the square 90 degrees and repeat.
                for value in sorted_allow_values:
                    i, j = np.where(stencil == value)
                    decrypted_text += str(square[i[0], j[0]])

                stencil = np.rot90(stencil, -1)

        return decrypted_text

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
                raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")
