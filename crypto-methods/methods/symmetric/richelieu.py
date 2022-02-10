
def encrypt(
        text: str,
        key: list[list[int]]
) -> str:
    encrypted_text = ""

    text_index = 0
    key_index = 0

    while True:
        subkey = key[key_index]

        if text_index + len(subkey) > len(text):
            encrypted_text += text[text_index::]
            break

        substr = text[text_index:text_index + len(subkey)]

        for i in subkey:
            encrypted_text += substr[i - 1]

        text_index += len(subkey)
        key_index = (key_index + 1) % len(key)

    return encrypted_text


def make(
        text: str,
        key: list[list[int]],
):
    return encrypt(text, key)
