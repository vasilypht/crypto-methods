import subprocess
from typing import Iterable


def get_alphabet_by_letter(
        letter: str,
        alphabets: dict[str, str]
) -> tuple[str, str] or None:
    """
    A function to find an alphabet from a dictionary with different 
    alphabets given a given letter.

    The first argument is the letter whose alphabet is to be found. 
    The letter can be in any case. The second argument is a dictionary
    that contains the language of the alphabet (enumeration) as a key,
    and a string with the alphabet itself as a value.

    Returns a tuple (language, alphabet) on success, None on failure.
    """
    letter = letter.lower()

    for lang, alphabet in alphabets.items():
        if letter in alphabet:
            return lang, alphabet

    return None


def get_letters_alphabetically(
        string: str,
        alphabet: Iterable[str]
) -> tuple[str, list[int]]:
    """
    A function to get letters from the given alphabet, as well as the
    indices at which these letters stand in the string.

    The first argument is the string in which the letters will be searched.
    The second argument is the alphabet to search for.

    Returns a tuple (found letters in the original case, indices where 
    the letters were in the string) on success, Nothing on failure.
    """
    indices = []

    letters = ""
    for i, letter in enumerate(string):
        if letter.lower() in alphabet:
            letters += letter
            indices.append(i)

    return letters, indices


def gen_prime(n: int = 1024) -> int:
    """
    The function of generating prime numbers of a given dimension.

    To generate prime numbers, the opensl program is used, if
    the program is missing, an exception will occur.

    n
        The number of bits in the prime to be generated. When generating prime
        numbers with a small number of bits (<50), the function will return the same number.
    """
    if not isinstance(n, int):
        raise TypeError("The function parameter must be an integer!")

    result = subprocess.run(["openssl", "prime", "-generate", "-bits", str(n)],
                            capture_output=True, timeout=5, check=True)

    return int(result.stdout)
