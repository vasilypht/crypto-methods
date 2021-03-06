import sys
import os

from PyQt6.QtWidgets import (
    QApplication
)
from PyQt6.QtGui import (
    QIcon
)
from PyQt6.QtCore import (
    QDir,
    QFile,
    QIODevice,
    QTextStream
)

from app.gui.mainwindow import MainWindow

PROJECT_DIR = os.path.dirname(__file__)

QDir.addSearchPath("icons", PROJECT_DIR + "/resources/icons")
QDir.addSearchPath("styles", PROJECT_DIR + "/gui")


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
