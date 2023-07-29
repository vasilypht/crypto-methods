from typing import Final

from .rsa import RSADSWidget
from .elgamal import ElgamalDSWidget
from .gost341112 import GOST341112DSWidget

WIDGETS_SIGNATURES: Final = (
    RSADSWidget,
    ElgamalDSWidget,
    GOST341112DSWidget,
)
