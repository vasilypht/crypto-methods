import sys

from PyQt6 import QtWidgets, QtGui

from ui.mainwindow import Ui_MainWindow
from const import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        QtGui.QFontDatabase.addApplicationFont("fonts/SourceSansPro-Regular.ttf")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.treeWidget.clicked.connect(self.__tree_widget_item_clicked)

        self.__init_tree_widget()
        self.__init_stacked_widget_default()

    def __tree_widget_item_clicked(self):
        item = self.ui.treeWidget.currentItem()
        parent = item.parent()

        try:
            path = f"./{parent.text(0)}/{item.text(0)}"
        except AttributeError:
            path = f"./{item.text(0)}"

        self.ui.group_box_2.setTitle(path)
        self.ui.stackedWidget.setCurrentIndex(TABLE_TASK_NAME_ID.get(item.text(0), 0))

    def __init_tree_widget(self):
        items = []
        for key, values in TABLE_TASK_NAMES.items():
            item = QtWidgets.QTreeWidgetItem((key,))
            for value in values:
                child = QtWidgets.QTreeWidgetItem((value,))
                item.addChild(child)
            items.append(item)
        self.ui.treeWidget.insertTopLevelItems(0, items)

    def __init_stacked_widget_default(self):
        self.ui.group_box_2.setTitle("Cryptographic methods")
        self.ui.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
