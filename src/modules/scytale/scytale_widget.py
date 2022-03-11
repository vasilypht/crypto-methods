import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget
)

from .scytale_ui import Ui_scytale


class ScytaleWidget(QWidget):
    def __init__(self):
        super(ScytaleWidget, self).__init__()
        self.ui = Ui_scytale()
        self.ui.setupUi(self)

        self.title = "Scytale"
        self.group = "Symmetric encryption"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScytaleWidget()
    window.show()

    sys.exit(app.exec())
