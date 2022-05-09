import sys

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

QDir.addSearchPath("icons", "resources/icons")
QDir.addSearchPath("styles", "gui")


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons:crypto-methods.png"))

    style_file = QFile("styles:style.css")

    if style_file.isOpen():
        style_file.open(QIODevice.OpenModeFlag.ReadOnly)
        app.setStyleSheet(QTextStream(style_file).readAll())
        style_file.close()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
