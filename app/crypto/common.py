from enum import (
    Enum,
    auto
)


class EncProc(Enum):
    ENCRYPT = auto()
    DECRYPT = auto()

    @staticmethod
    def from_str(value: str):
        match value.lower():
            case "encrypt":
                return EncProc.ENCRYPT

            case "decrypt":
                return EncProc.DECRYPT

            case _:
                raise NotImplementedError()


class Languages(Enum):
    ENGLISH = auto()
    RUSSIAN = auto()

    @staticmethod
    def from_str(value: str):
        match value.lower():
            case "english":
                return Languages.ENGLISH

            case "russian":
                return Languages.RUSSIAN

            case _:
                raise NotImplementedError()


class TextStyle(Enum):
    MATH = auto()
    COMMON = auto()
    LITERATURE = auto()

    @staticmethod
    def from_str(value: str):
        match value.lower():
            case "math":
                return TextStyle.MATH

            case "common":
                return TextStyle.COMMON

            case "literature":
                return TextStyle.LITERATURE

            case _:
                raise NotImplementedError()

