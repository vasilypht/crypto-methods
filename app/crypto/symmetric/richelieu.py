import re


class RichelieuError(Exception):
    pass


class Richelieu:
    def __init__(self, key: str):
        if not key:
            raise RichelieuError("The key is missing!")

        if not re.match(r"^\(\d+(,\d+|\)\(\d+)*\)$", key):
            raise RichelieuError("Invalid key entered!")

        self.key = self._parse_key(key)
        pass

    @staticmethod
    def _parse_key(key: str) -> tuple:
        # parse key str
        key_list = []
        for subkey in key.strip("()").split(")("):
            key_list.append(tuple(map(int, subkey.split(","))))

        # check range
        for subkey in key_list:
            for i in range(1, len(subkey) + 1):
                if i not in subkey:
                    raise RichelieuError("Invalid key entered!")

        return tuple(key_list)

    def _transform(self, text: str, mode: str = "encrypt") -> str:
        """Richelieu cipher. Encryption/decryption function.

        Args:
            text: text to be encrypted/decrypted.
            mode: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        if not text:
            raise RichelieuError("Input text is empty!")

        text_list: list[str] = list(text)

        text_index = 0
        key_index = 0

        while True:
            subkey = self.key[key_index]

            if text_index + len(subkey) > len(text):
                break

            substr = text[text_index:text_index + len(subkey)]

            for i, k in enumerate(subkey):
                match mode:
                    case "encrypt":
                        text_list[text_index + k - 1] = substr[i]

                    case "decrypt":
                        text_list[text_index + i] = substr[k - 1]

                    case _:
                        raise RichelieuError(f"Invalid processing type! -> {mode}")

            text_index += len(subkey)
            key_index = (key_index + 1) % len(self.key)

        return "".join(text_list)

    def encrypt(self, text: str) -> str:
        """Richelieu cipher. Interface for calling encryption functions.

        Args:
            text: text to be encrypted.

        Returns:
            Encrypted string.
        """
        return self._transform(text, "encrypt")

    def decrypt(self, text: str) -> str:
        """Richelieu cipher. Interface for calling decryption functions.

        Args:
            text: text to be decrypted.

        Returns:
            Decrypted string.
        """
        return self._transform(text, "decrypt")

    def make(self, text: str, mode: str = "encrypt") -> str:
        """Richelieu cipher. Interface for calling encryption/decryption functions.

        Args:
            text: text to be encrypted/decrypted.
            mode: encryption or decryption (default "encrypt").

        Returns:
            Encrypted or decrypted string.
        """
        match mode:
            case "encrypt":
                return self._transform(text, "encrypt")

            case "decrypt":
                return self._transform(text, "decrypt")

            case _:
                raise RichelieuError(f"Invalid processing type! -> {mode}")
