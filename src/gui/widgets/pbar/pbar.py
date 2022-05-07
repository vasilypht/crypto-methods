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
        self.setMaximumSize(400, 40)
        self.setMinimumSize(400, 40)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close_clicked.emit()

    def signal_handler(self, option: tuple):
        match option:
            case "current_value", value:
                self.setValue(value)

            case "min_value", value:
                self.setMinimum(value)

            case "max_value", value:
                self.setMaximum(value)

            case "range", min_value, max_value:
                self.setRange(min_value, max_value)

            case "show", *args:
                self.show()

            case "close", *args:
                self.close()
