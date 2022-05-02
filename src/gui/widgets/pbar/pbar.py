from PyQt6.QtWidgets import (
    QProgressBar
)
from PyQt6.QtCore import (
    pyqtSignal
)
from PyQt6.QtGui import (
    QCloseEvent
)


class PBar(QProgressBar):
    close_clicked = pyqtSignal()

    def __init__(self):
        super(PBar, self).__init__()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close_clicked.emit()
