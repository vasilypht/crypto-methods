def encrypt(text: str, n: int, m: int) -> str:
    lines_list: list[list[str]] = []

    for i in range(n):
        line = list(text[i * m:(i + 1) * m])
        line += (m - len(line)) * [" "]
        lines_list.append(line)

    flip_lines_list = [i for i in zip(*lines_list)]
    return ''.join(''.join(i) for i in flip_lines_list).rstrip()


def decrypt(text: str, n: int) -> str:
    lines_list: list[str] = []

    for i in range(n):
        line = text[i:len(text):n]
        lines_list.append(line)

    return ''.join(lines_list).rstrip()


def make(
        text: str,
        n: int,
        m: int,
        processing_type: str = "Encrypt",
        auto_m: bool = True
) -> str:
    if n < 0 or m < 0:
        raise Exception("'n' and 'm' must be positive!")

    if auto_m:
        m = (len(text) - 1) // n + 1

    match processing_type:
        case "Encrypt":
            return encrypt(text, n, m)

        case "Decrypt":
            return decrypt(text, n)

        case _:
            return ""
