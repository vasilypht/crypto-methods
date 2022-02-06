from typing import Final
from random import random

ENG_LETTER_INDEX: Final = {
    "A": (1, 1), "B": (2, 1), "C": (3, 1), "D": (4, 1),              "E": (5, 1),
    "F": (1, 2), "G": (2, 2), "H": (3, 2), "I": (4, 2), "J": (4, 2), "K": (5, 2),
    "L": (1, 3), "M": (2, 3), "N": (3, 3), "O": (4, 3),              "P": (5, 3),
    "Q": (1, 4), "R": (2, 4), "S": (3, 4), "T": (4, 4),              "U": (5, 4),
    "V": (1, 5), "W": (2, 5), "X": (3, 5), "Y": (4, 5),              "Z": (5, 5)
}

ENG_INDEX_LETTER: Final = {
    (1, 1): ("A",), (2, 1): ("B",), (3, 1): ("C",), (4, 1): ("D",),     (5, 1): ("E",),
    (1, 2): ("F",), (2, 2): ("G",), (3, 2): ("H",), (4, 2): ("I", "J"), (5, 2): ("K",),
    (1, 3): ("L",), (2, 3): ("M",), (3, 3): ("N",), (4, 3): ("O",),     (5, 3): ("P",),
    (1, 4): ("Q",), (2, 4): ("R",), (3, 4): ("S",), (4, 4): ("T",),     (5, 4): ("U",),
    (1, 5): ("V",), (2, 5): ("W",), (3, 5): ("X",), (4, 5): ("Y",),     (5, 5): ("Z",)
}

RUS_LETTER_INDEX: Final = {
    "А": (1, 1),              "Б": (2, 1),              "В": (3, 1),              "Г": (4, 1), "Д": (5, 1),
    "Е": (1, 2), "Э": (1, 2), "Ж": (2, 2), "З": (2, 2), "И": (3, 2), "Й": (3, 2), "К": (4, 2), "Л": (5, 2),
    "М": (1, 3),              "Н": (2, 3),              "О": (3, 3),              "П": (4, 3), "Р": (5, 3), "С": (5, 3),
    "Т": (1, 4),              "У": (2, 4),              "Ф": (3, 4), "Х": (3, 4), "Ц": (4, 4), "Ч": (5, 4),
    "Ш": (1, 5), "Щ": (1, 5), "Ы": (2, 5),              "Ь": (3, 5),              "Ю": (4, 5), "Я": (5, 5)
}

RUS_INDEX_LETTER: Final = {
    (1, 1): ("А",),     (2, 1): ("Б",),     (3, 1): ("В",),     (4, 1): ("Г",), (5, 1): ("Д",),
    (1, 2): ("Е", "Э"), (2, 2): ("Ж", "З"), (3, 2): ("И", "Й"), (4, 2): ("К",), (5, 2): ("Л",),
    (1, 3): ("М",),     (2, 3): ("Н",),     (3, 3): ("О",),     (4, 3): ("П",), (5, 3): ("P", "С"),
    (1, 4): ("Т",),     (2, 4): ("У",),     (3, 4): ("Ф", "Х"), (4, 4): ("Ц",), (5, 4): ("Ч",),
    (1, 5): ("Ш", "Щ"), (2, 5): ("Ы",),     (3, 5): ("Ь",),     (4, 5): ("Ю",), (5, 5): ("Я",)
}


def method_1(text: str, processing_type: str = "Encrypt") -> str:
    processed_text = ""

    for char in text:
        char_upper = char.upper()

        for letter_index, index_letter in ((ENG_LETTER_INDEX, ENG_INDEX_LETTER),
                                           (RUS_LETTER_INDEX, RUS_INDEX_LETTER)):
            if char_upper not in letter_index.keys():
                continue

            i, j = letter_index.get(char_upper)

            match processing_type:
                case "Encrypt":
                    if j == 5:
                        j = 1
                    else:
                        j += 1

                case "Decrypt":
                    if j == 1:
                        j = 5
                    else:
                        j -= 1

                case _:
                    raise Exception("Invalid processing type!")

            chars = index_letter.get((i, j))
            char_upper = chars[round(random())] if len(chars) == 2 else chars[0]
            break

        if char.islower():
            char = char_upper.lower()
        else:
            char = char_upper

        processed_text += char

    return processed_text


def _get_indices(text: str) -> tuple[list, list, list]:
    letter_indices = []

    indices_i = []
    indices_j = []

    for char_index, char in enumerate(text):
        char_upper = char.upper()

        for letter_index, index_letter, lang in ((ENG_LETTER_INDEX, ENG_INDEX_LETTER, "ENG"),
                                                 (RUS_LETTER_INDEX, RUS_INDEX_LETTER, "RUS")):
            if char_upper not in letter_index.keys():
                continue

            letter_indices.append((char_index, lang))

            i, j = letter_index.get(char_upper)
            indices_i.append(i)
            indices_j.append(j)
            break

    return letter_indices, indices_i, indices_j


def _replace_letters(
        text: str,
        letter_indices: list[tuple[int, str]],
        indices: list[tuple[int, int]]
):
    list_text: list[str] = list(text)

    # i - for letter_indices
    # k - for indices_ij
    for i, (letter_i, letter_j) in enumerate(indices):
        letter_index, lang = letter_indices[i]

        match lang:
            case "ENG":
                letters = ENG_INDEX_LETTER.get((letter_i, letter_j))

            case "RUS":
                letters = RUS_INDEX_LETTER.get((letter_i, letter_j))

            case _:
                raise Exception("Wrong language!")

        letter = letters[round(random())] if len(letters) == 2 else letters[0]
        if list_text[letter_index].islower():
            letter = letter.lower()

        list_text[letter_index] = letter

    return ''.join(list_text)


def method_2(text: str, processing_type: str = "Encrypt") -> str:
    letter_indices, indices_i, indices_j = _get_indices(text)

    match processing_type:
        case "Encrypt":
            indices_ij = indices_i + indices_j
            indices = [(indices_ij[i], indices_ij[i + 1]) for i in range(0, len(indices_ij), 2)]

        case "Decrypt":
            indices_ij = [index for pair in zip(indices_i, indices_j) for index in pair]
            k = len(indices_ij) // 2
            indices = list(zip(indices_ij[:k:], indices_ij[k::]))

        case _:
            raise Exception("Invalid processing type!")

    processed_text = _replace_letters(text, letter_indices, indices)

    return processed_text


def method_3(text: str, shift: int = 1, processing_type: str = "Encrypt") -> str:
    if shift <= 0 or shift % 2 == 0:
        raise Exception("Invalid shift value! Value must be odd!")

    letter_indices, indices_i, indices_j = _get_indices(text)

    match processing_type:
        case "Encrypt":
            indices_ij = indices_i + indices_j
            indices_ij = indices_ij[shift::] + indices_ij[:shift:]
            indices = [(indices_ij[i], indices_ij[i + 1]) for i in range(0, len(indices_ij), 2)]

        case "Decrypt":
            indices_ij = [index for pair in zip(indices_i, indices_j) for index in pair]
            indices_ij = indices_ij[len(indices_ij) - shift:] + indices_ij[:len(indices_ij) - shift:]
            k = len(indices_ij) // 2
            indices = list(zip(indices_ij[:k:], indices_ij[k::]))

        case _:
            raise Exception("Invalid processing type!")

    processed_text = _replace_letters(text, letter_indices, indices)

    return processed_text


def make(text: str,
         method: str = "Method 1",
         shift: int = 1,
         processing_type: str = "Encrypt") -> str:

    match method:
        case "Method 1":
            return method_1(text, processing_type)

        case "Method 2":
            return method_2(text, processing_type)

        case "Method 3":
            return method_3(text, shift, processing_type)

        case _:
            raise Exception("Invalid method name!")
