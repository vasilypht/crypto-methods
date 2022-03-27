from PyQt6.QtWidgets import (
    QMainWindow,
    QTreeWidgetItem,
    QWidget
)
from PyQt6.QtGui import (
    QIcon
)

from .mainwindow_ui import Ui_MainWindow

from .defmodules import WIDGETS_DEFAULT
from .symmetric import WIDGETS_SYMMETRIC
from .asymmetric import WIDGETS_ASYMMETRIC
from .cryptotools import WIDGETS_CRYPTOTOOLS

WIDGETS_CIPHERS = {
    "Symmetric ciphers": WIDGETS_SYMMETRIC,
    "Asymmetric ciphers": WIDGETS_ASYMMETRIC,
    "Crypto tools": WIDGETS_CRYPTOTOOLS
}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Crypto methods")

        self.ui.splitter.setStretchFactor(1, 1)

        self.ui.tree_widget.clicked.connect(self.tree_widget_item_clicked)

        self.load_modules()

    def load_modules(self):
        # Load default modules
        for widget in WIDGETS_DEFAULT:
            self.ui.stacked_widget.addWidget(widget())

        # Load other widgets
        items = []

        for title, widgets in WIDGETS_CIPHERS.items():
            parent = QTreeWidgetItem((title,))
            parent.setIcon(0, QIcon("icons:folder.png"))

            children = []
            for widget in widgets:
                widget = widget()

                self.ui.stacked_widget.addWidget(widget)

                child = QTreeWidgetItem((widget.title,))
                child.setIcon(0, QIcon("icons:file.png"))
                child.setData(1, 1, widget)
                children.append(child)

            parent.addChildren(children)
            items.append(parent)

        self.ui.tree_widget.invisibleRootItem().addChildren(items)

    def tree_widget_item_clicked(self):
        item = self.ui.tree_widget.currentItem()
        widget = item.data(1, 1)

        match widget:
            case QWidget():
                self.ui.group_box_right.setTitle(item.text(0))
                self.ui.stacked_widget.setCurrentWidget(widget)

            case _:
                pass
