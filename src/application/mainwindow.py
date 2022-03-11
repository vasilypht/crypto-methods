from PyQt6.QtWidgets import (
    QMainWindow,
    QTreeWidgetItem,
)
from PyQt6.QtGui import (
    QIcon
)

from src.application.mainwindow_ui import Ui_MainWindow
from src.modules import WIDGETS_CIPHERS


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.splitter.setStretchFactor(1, 1)

        self.ui.tree_widget.clicked.connect(self.tree_widget_item_clicked)
        self.load_modules()

    def load_modules(self):
        items = []

        for widget in WIDGETS_CIPHERS:
            widget = widget()
            self.ui.stacked_widget.addWidget(widget)

            item = QTreeWidgetItem((widget.title,))
            item.setIcon(0, QIcon("icons:file.png"))
            item.setData(1, 1, widget)
            items.append(item)

        self.ui.tree_widget.invisibleRootItem().addChildren(items)

    def tree_widget_item_clicked(self):
        item = self.ui.tree_widget.currentItem()
        widget = item.data(1, 1)
        self.ui.group_box_right.setTitle(widget.title)
        self.ui.stacked_widget.setCurrentWidget(widget)
