from typing import Final

from .rsa import RSAWidget
from .elgamal import ElgamalWidget

WIDGETS_ASYMMETRIC: Final = (
    RSAWidget,
    ElgamalWidget
)
