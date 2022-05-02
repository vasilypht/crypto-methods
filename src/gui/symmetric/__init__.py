from typing import Final

from .atbash import AtbashWidget
from .scytale import ScytaleWidget
from .polybius_square import PolybiusSquareWidget
from .caesar import CaesarWidget
from .cardan_grille import CardanGrilleWidget
from .richelieu import RichelieuWidget
from .alberti_disc import AlbertiDiscWidget
from .gronsfeld import GronsfeldWidget
from .vigenere import VigenereWidget
from .playfair import PlayfairWidget
from .hill import HillWidget
from .vernam import VernamWidget
from .xor import XORWidget

WIDGETS_SYMMETRIC: Final = (
    AtbashWidget,
    ScytaleWidget,
    PolybiusSquareWidget,
    CaesarWidget,
    CardanGrilleWidget,
    RichelieuWidget,
    AlbertiDiscWidget,
    GronsfeldWidget,
    VigenereWidget,
    PlayfairWidget,
    HillWidget,
    VernamWidget,
    XORWidget
)
