from enum import Enum, auto

from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)


class BaseQThread(QThread):
    pbar = pyqtSignal(tuple)
    message = pyqtSignal(tuple)

    class MessageType(Enum):
        WARNING = auto(),
        INFORMATION = auto(),
        CRITICAL = auto(),
        QUESTION = auto(),

    def __init__(self, *args, **kwargs):
        super(BaseQThread, self).__init__(*args, **kwargs)

    def close(self):
        pass
