from typing import Final

from .diffie_hellman import DiffieHellmanWidget
from .shamir import ShamirWidget


WIDGETS_CRYPTOPROTOCOLS: Final = (
    DiffieHellmanWidget,
    ShamirWidget
)
