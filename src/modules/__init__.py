from typing import Final

from .atbash.atbash_widget import AtbashWidget
from .scytale.scytale_widget import ScytaleWidget
from .polybius_square.polybius_square_widget import PolybiusSquareWidget

WIDGETS_CIPHERS: Final = (
    AtbashWidget,
    ScytaleWidget,
    PolybiusSquareWidget
)