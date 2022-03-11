from typing import Final

from .atbash.atbash_widget import AtbashWidget
from .scytale.scytale_widget import ScytaleWidget

WIDGETS_CIPHERS: Final = (
    AtbashWidget,
    ScytaleWidget
)