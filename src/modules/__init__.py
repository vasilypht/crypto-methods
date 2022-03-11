from typing import Final

from .atbash.atbash_widget import AtbashWidget
from .scytale.scytale_widget import ScytaleWidget
from .polybius_square.polybius_square_widget import PolybiusSquareWidget
from .caesar.caesar_widget import CaesarWidget
from .cardan_grille.cardan_grille_widget import CardanGrilleWidget
from .richelieu.richelieu_widget import RichelieuWidget
from .alberti_disc.alberti_disc_widget import AlbertiDiscWidget
from .gronsfeld.gronsfeld_widget import GronsfeldWidget
from .vigenere.vigenere_widget import VigenereWidget
from .playfair.playfair_widget import PlayfairWidget
from .hill.hill_widget import HillWidget

WIDGETS_CIPHERS: Final = (
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
    HillWidget
)
