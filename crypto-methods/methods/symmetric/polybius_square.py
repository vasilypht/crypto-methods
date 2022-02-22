from random import randint

from ..const import (
    PS_RUS_LETTER_INDEX,
    PS_RUS_INDEX_LETTER,
    PS_ENG_LETTER_INDEX,
    PS_ENG_INDEX_LETTER
)


class PolybiusSquareError(Exception):
    pass


def get_square_by_letter(letter: str) -> tuple[dict, dict, str] or None:
    """Function to determine the language of a square by letter.

    Args:
        letter: any character.

    Returns:
        Square in the form of dictionaries and language, otherwise None.
    """
    if not letter:
        return None

    for letter_index, index_letter, lang in ((PS_ENG_LETTER_INDEX, PS_ENG_INDEX_LETTER, "en"),
                                             (PS_RUS_LETTER_INDEX, PS_RUS_INDEX_LETTER, "ru")):
        if letter.upper() in letter_index.keys():
            return letter_index, index_letter, lang

    return None


def method_1(text: str, mode: str = "encrypt") -> str:
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

        if (square := get_square_by_letter(letter)) is None:
            continue

        letter_index, index_letter, _ = square
        letter_i, letter_j = letter_index.get(letter.upper())

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

        new_letters = index_letter.get((letter_i, letter_j))
        new_letter = new_letters[randint(0, 1)] if len(new_letters) == 2 else new_letters[0]

        if letter.islower():
            new_letter = new_letter.lower()

        text_list[i] = new_letter

    return "".join(text_list)


def get_indices_from_square(text: str) -> tuple[list, tuple[list, list]]:
    """A function to extract characters from text that can be processed by methods.

    Args:
        text: text from which letters will be extracted for further processing.

    Returns:
        A list containing pairs (the index of a letter in the source text and its language),
            as well as a tuple with the indices of these letters in squares.
    """
    # pair (letter_index, lang), (...), ...
    letter_indices = []

    indices_i = []
    indices_j = []

    for i, letter in enumerate(text):
        if (square := get_square_by_letter(letter)) is None:
            continue

        letter_index, index_letter, lang = square

        letter_indices.append((i, lang))
        letter_i, letter_j = letter_index.get(letter.upper())
        indices_i.append(letter_i)
        indices_j.append(letter_j)

    return letter_indices, (indices_i, indices_j)


def replace_letters_by_indices(
        text: str,
        letter_indices: list[tuple[int, str]],
        square_indices: list[tuple[int, int]]
):
    """A function to replace certain letters in the text with new ones.

    Args:
        text: the text in which the letters will be changed.
        letter_indices: a list containing pairs (the index of a letter in the source text and its language)
        square_indices: new indexes by which new letters in the square will be found.

    Returns:
        String with changed letters.
    """
    list_text: list[str] = list(text)

    # i - for letter_indices
    # k - for indices_ij
    for i, (letter_i, letter_j) in enumerate(square_indices):
        letter_index, lang = letter_indices[i]

        match lang:
            case "en":
                letters = PS_ENG_INDEX_LETTER.get((letter_i, letter_j))

            case "ru":
                letters = PS_RUS_INDEX_LETTER.get((letter_i, letter_j))

            case _:
                raise PolybiusSquareError(f"Wrong language! -> {lang}")

        new_letter = letters[randint(0, 1)] if len(letters) == 2 else letters[0]

        if list_text[letter_index].islower():
            new_letter = new_letter.lower()

        list_text[letter_index] = new_letter

    return "".join(list_text)


def method_2(text: str, mode: str = "encrypt") -> str:
    """Polybius Square. Method 2. Function for encryption and decryption.

    Args:
        text: text to encrypt or decrypt.
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise PolybiusSquareError("Input text is empty!")

    letter_indices, (indices_i, indices_j) = get_indices_from_square(text)

    match mode:
        case "encrypt":
            indices_ij = indices_i + indices_j
            indices = [(indices_ij[i], indices_ij[i + 1]) for i in range(0, len(indices_ij), 2)]

        case "decrypt":
            indices_ij = [index for pair in zip(indices_i, indices_j) for index in pair]
            k = len(indices_ij) // 2
            indices = list(zip(indices_ij[:k:], indices_ij[k::]))

        case _:
            raise PolybiusSquareError(f"Invalid processing type! -> {mode}")

    processed_text = replace_letters_by_indices(text, letter_indices, indices)
    return processed_text


def method_3(text: str, shift: int = 1, mode: str = "encrypt") -> str:
    """Polybius Square. Method 3. Function for encryption and decryption.

    Args:
        text: text to encrypt or decrypt.
        shift: odd number for third method (default 1).
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise PolybiusSquareError("Input text is empty!")

    if shift <= 0 or shift % 2 == 0:
        raise PolybiusSquareError("Invalid shift value! Value must be positive and odd!")

    shift %= len(text)
    letter_indices, (indices_i, indices_j) = get_indices_from_square(text)

    match mode:
        case "encrypt":
            indices_ij = indices_i + indices_j
            indices_ij = indices_ij[shift::] + indices_ij[:shift:]
            indices = [(indices_ij[i], indices_ij[i + 1]) for i in range(0, len(indices_ij), 2)]

        case "decrypt":
            indices_ij = [index for pair in zip(indices_i, indices_j) for index in pair]
            indices_ij = indices_ij[len(indices_ij) - shift:] + indices_ij[:len(indices_ij) - shift:]
            k = len(indices_ij) // 2
            indices = list(zip(indices_ij[:k:], indices_ij[k::]))

        case _:
            raise PolybiusSquareError(f"Invalid processing type! -> {mode}")

    processed_text = replace_letters_by_indices(text, letter_indices, indices)
    return processed_text


def encrypt(text: str, shift: int = 1, method: str = "method 1") -> str:
    """Polybius square cipher. Interface for calling encryption functions.

    Args:
        text: text to be encrypted.
        shift: odd number for third method (default 1).
        method: encryption method (default "method 1").

    Returns:
        Encrypted string.
    """
    match method:
        case "method 1":
            return method_1(text, "encrypt")

        case "method 2":
            return method_2(text, "encrypt")

        case "method 3":
            return method_3(text, shift, "encrypt")

        case _:
            raise PolybiusSquareError(f"Invalid method type! -> {method}")


def decrypt(text: str, shift: int = 1, method: str = "method 1") -> str:
    """Polybius square cipher. Interface for calling decryption functions.

    Args:
        text: text to be decrypted.
        shift: odd number for third method (default 1).
        method: encryption method (default "method 1").

    Returns:
        Decrypted string.
    """
    match method:
        case "method 1":
            return method_1(text, "decrypt")

        case "method 2":
            return method_2(text, "decrypt")

        case "method 3":
            return method_3(text, shift, "decrypt")

        case _:
            raise PolybiusSquareError(f"Invalid method type! -> {method}")


def make(
        text: str,
        shift: int = 1,
        method: str = "method 1",
        mode: str = "encrypt"
) -> str:
    """Polybius square cipher. Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        shift: odd number for third method (default 1).
        method: encryption method (default "method 1").
        mode: encryption or decryption (default "encrypt").

    Returns:
        Encrypted or decrypted string.
    """
    match mode:
        case "encrypt":
            return encrypt(text, shift, method)

        case "decrypt":
            return decrypt(text, shift, method)

        case _:
            raise PolybiusSquareError(f"Invalid processing type! -> {mode}")
