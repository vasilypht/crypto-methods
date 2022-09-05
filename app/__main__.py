import sys
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import (
    QDir,
    QFile,
    QIODevice,
    QTextStream
)

APP_PATH = os.path.dirname(__file__)
PROJECT_PATH = str(Path(APP_PATH).parent)

sys.path.append(APP_PATH)
sys.path.append(PROJECT_PATH)

QDir.addSearchPath("icons", APP_PATH + "/resources/icons")
QDir.addSearchPath("styles", APP_PATH + "/gui")

from app.gui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons:crypto-methods.png"))

    style_file = QFile("styles:style.css")
    style_file.open(QIODevice.OpenModeFlag.ReadOnly)

    if style_file.isOpen():
        app.setStyleSheet(QTextStream(style_file).readAll())
        style_file.close()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
