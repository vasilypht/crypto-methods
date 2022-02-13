
def encrypt(
        text: str,
        key: list[list[int]]
) -> str:
    encrypted_text = list(text)

    text_index = 0
    key_index = 0

    while True:
        subkey = key[key_index]

        if text_index + len(subkey) > len(text):
            break

        substr = text[text_index:text_index + len(subkey)]

        for i, k in enumerate(subkey):
            encrypted_text[text_index + k - 1] = substr[i]

        text_index += len(subkey)
        key_index = (key_index + 1) % len(key)

    return "".join(encrypted_text)


def decrypt(
        text: str,
        key: list[list[int]]
) -> str:
    decrypted_text = list(text)

    text_index = 0
    key_index = 0

    while True:
        subkey = key[key_index]

        if text_index + len(subkey) > len(text):
            break

        substr = text[text_index:text_index + len(subkey)]

        for i, k in enumerate(subkey):
            decrypted_text[text_index + i] = substr[k - 1]

        text_index += len(subkey)
        key_index = (key_index + 1) % len(key)

    return "".join(decrypted_text)


def make(
        text: str,
        key: list[list[int]],
        processing_type: str = "Encrypt"
) -> str:
    match processing_type:
        case "Encrypt":
            return encrypt(text, key)

        case "Decrypt":
            return decrypt(text, key)

        case _:
            raise Exception("Invalid processing type!")
