import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from PyQt6.QtWidgets import (
    QApplication
)
from PyQt6.QtGui import (
    QIcon
)
from PyQt6.QtCore import (
    QDir
)
import darkdetect

from src.gui.mainwindow import MainWindow

QDir.addSearchPath("icons", "resources/icons")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons:crypto-methods.png"))

    if darkdetect.isDark():
        theme_path = "gui/styles/dark-theme.css"
    else:
        theme_path = "gui/styles/light-theme.css"

    with open(theme_path) as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
