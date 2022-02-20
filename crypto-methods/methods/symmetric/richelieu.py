
def transform(text: str, key: list[list[int]], mode: bool = True) -> str:
    text_list: list[str] = list(text)

    text_index = 0
    key_index = 0

    while True:
        subkey = key[key_index]

        if text_index + len(subkey) > len(text):
            break

        substr = text[text_index:text_index + len(subkey)]

        for i, k in enumerate(subkey):
            if mode:
                text_list[text_index + k - 1] = substr[i]
            else:
                text_list[text_index + i] = substr[k - 1]

        text_index += len(subkey)
        key_index = (key_index + 1) % len(key)

    return "".join(text_list)


def encrypt(text: str, key: list[list[int]]) -> str:
    return transform(text, key, True)


def decrypt(text: str, key: list[list[int]]) -> str:
    return transform(text, key, False)


def make(
        text: str,
        key: list[list[int]],
        processing_type: str = "encrypt"
) -> str:
    match processing_type:
        case "encrypt":
            return encrypt(text, key)

        case "decrypt":
            return decrypt(text, key)

        case _:
            raise Exception("Invalid processing type!")
