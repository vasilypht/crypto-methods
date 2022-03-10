from ..const import (
    KOI8R_STOPBYTES
)


class VernamError(Exception):
    pass


def transform(text: str, key: str) -> str:
    """Vernam cipher (charset 'KOI8-r'). Encryption/decryption function.

    Args:
        text: text to be encrypted/decrypted.
        key: arbitrary character set.

    Returns:
        Encrypted or decrypted string.
    """
    if not text:
        raise VernamError("Input text is empty!")

    if not key:
        raise VernamError("The key is missing!")

    # attempt to change the encoding of the input text
    try:
        text_bytes = bytearray(text, encoding="KOI8-r")

    except UnicodeEncodeError:
        raise VernamError("Invalid character in input text! (KOI8-r)")

    # attempt to change key encoding
    try:
        key_bytes = bytearray(key, encoding="KOI8-r")

    except UnicodeEncodeError:
        raise VernamError("Invalid character in key! (KOI8-r)")

    for i in range(len(text_bytes)):
        text_bytes[i] ^= key_bytes[i % len(key_bytes)]
        if text_bytes[i] in KOI8R_STOPBYTES:
            raise VernamError("Service byte received! Change the key or text.")

    try:
        modified_text = text_bytes.decode("KOI8-r")

    except UnicodeDecodeError:
        raise VernamError("Decoding error! (from 'KOI8-r')")

    return modified_text


def make(text: str, key: str) -> str:
    """Vernam cipher (charset 'KOI8-r'). Interface for calling encryption/decryption functions.

    Args:
        text: text to be encrypted/decrypted.
        key: arbitrary character set.

    Returns:
        Encrypted or decrypted string.
    """
    return transform(text, key)
