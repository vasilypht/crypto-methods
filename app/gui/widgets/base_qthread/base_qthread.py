from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)


class BaseQThread(QThread):
    pbar = pyqtSignal(tuple)
    message = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(BaseQThread, self).__init__(*args, **kwargs)

    def close(self):
        pass
