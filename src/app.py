import sys

from PyQt6.QtWidgets import (
    QApplication
)
from PyQt6.QtGui import (
    QIcon
)
from PyQt6.QtCore import (
    QDir
)

from src.application.mainwindow import MainWindow

QDir.addSearchPath("icons", "resources/icons")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons:crypto-methods.png"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
