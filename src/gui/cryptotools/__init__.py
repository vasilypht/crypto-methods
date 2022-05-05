from typing import Final

from .freqanalysis import FreqAnalysisWidget
from .index_of_coincidence import ICWidget
from .kasiski import KasiskiWidget

WIDGETS_CRYPTOTOOLS: Final = (
    FreqAnalysisWidget,
    ICWidget,
    KasiskiWidget
)
