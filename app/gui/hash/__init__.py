from typing import Final

from .md5 import MD5Widget
from .sha1 import SHA1Widget
from .gost341112 import GOST341112Widget

WIDGETS_HASH: Final = (
    MD5Widget,
    SHA1Widget,
    GOST341112Widget,
)
