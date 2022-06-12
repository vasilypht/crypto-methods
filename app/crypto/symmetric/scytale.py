
class ScytaleError(Exception):
    pass


class Scytale:
    def __init__(self, n: int, m: int = None, auto_m: bool = True):
        if not auto_m and m is None:
            raise ScytaleError("You must set the value of 'm', or set the automatic calculation flag 'auto_m'!")

        if n <= 0:
            raise ScytaleError("'n' must be positive!")

        if m <= 0:
            raise ScytaleError("'n' must be positive!")

        self.n = n
        self.m = m
        self.auto_m = auto_m

    def encrypt(self, text: str) -> str:
        if not text:
            raise ScytaleError("Input text is empty!")

        if self.auto_m:
            self.m = (len(text) - 1) // self.n + 1

        lines_list: list[list[str]] = []

        for i in range(self.n):
            line = list(text[i * self.m:(i + 1) * self.m])
            line += (self.m - len(line)) * [" "]
            lines_list.append(line)

        flip_lines_list = [i for i in zip(*lines_list)]
        return "".join("".join(i) for i in flip_lines_list)

    def decrypt(self, text: str) -> str:
        if not text:
            raise ScytaleError("Input text is empty!")

        lines_list: list[str] = []

        for i in range(self.n):
            line = text[i:len(text):self.n]
            lines_list.append(line)

        return "".join(lines_list)

    def make(self, text: str, mode: str = "encrypt") -> str:
        match mode:
            case "encrypt":
                return self.encrypt(text)

            case "decrypt":
                return self.decrypt(text)

            case _:
                raise ScytaleError(f"Invalid processing type! -> {mode}")
