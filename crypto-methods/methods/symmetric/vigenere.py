from ..utils import (
    get_alphabet_by_letter
)


def transform(text: str, key: str, mode: bool = True) -> str:
    text_list: list[str] = list(text)

    for i in range(len(text)):
        letter_text = text_list[i]
        if (alphabet_lang_text := get_alphabet_by_letter(letter_text)) is None:
            continue

        letter_key = key[i % len(key)]
        if (alphabet_lang_key := get_alphabet_by_letter(letter_key)) is None:
            continue

        alphabet_letter_text, _ = alphabet_lang_text
        alphabet_letter_key, _ = alphabet_lang_key

        letter_text_index = alphabet_letter_text.index(letter_text.lower())
        letter_key_index = alphabet_letter_key.index(letter_key.lower())

        # choice of sign
        key_sign = 1 if mode else -1

        new_letter_text_index = (letter_text_index + letter_key_index * key_sign) % len(alphabet_letter_text)
        new_letter_text = alphabet_letter_text[new_letter_text_index]

        if letter_text.isupper():
            new_letter_text = new_letter_text.upper()

        text_list[i] = new_letter_text

    return "".join(text_list)


def encrypt(text: str, key: str) -> str:
    return transform(text, key, True)


def decrypt(text: str, key: str) -> str:
    return transform(text, key, False)


def make(text: str, key: str, mode: str) -> str:

    match mode:
        case "encrypt":
            return encrypt(text, key)

        case "decrypt":
            return decrypt(text, key)

        case _:
            raise Exception("Invalid processing type!")
