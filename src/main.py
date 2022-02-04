import sys

import yaml
from PyQt6 import QtWidgets, QtGui

from gui.mainwindow import Ui_MainWindow
from methods import symmetric as sym


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__config = None

        # General settings
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.treeWidget.clicked.connect(self.tree_widget_item_clicked)

        # page 1
        self.ui.page_1_button_calc.clicked.connect(self.page_1_button_calc_clicked)

        # page 2
        self.ui.page_2_check_box_columns.stateChanged.connect(self.page_2_check_box_check)
        self.ui.page_2_button_calc.clicked.connect(self.page_2_button_calc_clicked)

        self.__load_config()
        self.__init_tree_widget()
        self.__init_stacked_widget_default()

    def __load_config(self):
        try:
            with open("src/config.yaml", "r") as cfg:
                self.__config = yaml.safe_load(cfg)

        except IOError:
            QtWidgets.QMessageBox.critical(self, "Error!", "Failed to open config!")
            sys.exit(0)

    def tree_widget_item_clicked(self):
        item = self.ui.treeWidget.currentItem()
        parent = item.parent()

        try:
            path = f"./{parent.text(0)}/{item.text(0)}"
        except AttributeError:
            path = f"./{item.text(0)}"

        self.ui.group_box_right.setTitle(path)
        self.ui.stackedWidget.setCurrentIndex(self.__config["task id"].get(item.text(0), 0))

    def __init_tree_widget(self):
        items = []
        for key, values in self.__config["task names"].items():
            item = QtWidgets.QTreeWidgetItem((key,))
            for value in values:
                child = QtWidgets.QTreeWidgetItem((value,))
                item.addChild(child)
            items.append(item)
        self.ui.treeWidget.insertTopLevelItems(0, items)

    def __init_stacked_widget_default(self):
        self.ui.group_box_right.setTitle("Cryptographic methods")
        self.ui.stackedWidget.setCurrentIndex(0)

    def page_1_button_calc_clicked(self):
        input_text = self.ui.page_1_text_edit_input.toPlainText()
        processed_text = sym.atbash.encrypt(input_text)
        self.ui.page_1_text_edit_output.setText(processed_text)

    def page_2_check_box_check(self):
        if self.ui.page_2_check_box_columns.isChecked():
            self.ui.page_2_spin_box_columns.setDisabled(False)
            self.ui.page_2_check_box_columns.setStyleSheet("color: white")
        else:
            self.ui.page_2_spin_box_columns.setDisabled(True)
            self.ui.page_2_check_box_columns.setStyleSheet("color: grey")

    def page_2_button_calc_clicked(self):
        processed_text = sym.scytale.make(
            text=self.ui.page_2_text_edit_input.toPlainText(),
            n=self.ui.page_2_spin_box_rows.value(),
            m=self.ui.page_2_spin_box_columns.value(),
            processing_type=self.ui.page_2_combo_box_rows.currentText(),
            auto_m=not self.ui.page_2_check_box_columns.isChecked()
        )

        self.ui.page_2_text_edit_output.setText(processed_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("resources/icon/cyber-security.png"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
