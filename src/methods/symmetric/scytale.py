

def encrypt(text: str, n: int, m: int) -> str:
    lines_list: list[list[str]] = []

    for i in range(n):
        line = list(text[i*m:(i+1)*m])
        line += (m - len(line)) * [" "]
        lines_list.append(line)

    flip_lines_list = [i for i in zip(*lines_list)]
    return ''.join(''.join(i) for i in flip_lines_list)


def decrypt(text: str, n: int) -> str:
    lines_list: list[str] = []

    for i in range(n):
        line = text[i:len(text):n]
        lines_list.append(line)

    return ''.join(lines_list)
