import sys
import math

from PyQt6 import QtWidgets, QtGui
import yaml
import numpy as np

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

        # page 3
        self.ui.page_3_combo_box_method.currentIndexChanged.connect(self.page_3_combo_box_check)
        self.ui.page_3_button_calc.clicked.connect(self.page_3_button_calc_clicked)

        # page 4
        self.ui.page_4_button_calc.clicked.connect(self.page_4_button_calc_clicked)

        # page 5
        self.ui.page_5_button_gen_stencil.clicked.connect(self.page_5_button_gen_stencil_clicked)
        self.ui.page_5_button_calc.clicked.connect(self.page_5_button_calc_clicked)

        self.__load_config()
        self.__init_tree_widget()
        self.__init_stacked_widget_default()

    def __load_config(self):
        try:
            with open("config.yaml", "r") as cfg:
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
        processed_text = sym.atbash.make(
            text=self.ui.page_1_text_edit_input.toPlainText()
        )
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
            processing_type=self.ui.page_2_combo_box_type.currentText(),
            auto_m=not self.ui.page_2_check_box_columns.isChecked()
        )

        self.ui.page_2_text_edit_output.setText(processed_text)

    def page_3_combo_box_check(self):
        if self.ui.page_3_combo_box_method.currentText() == "Method 3":
            self.ui.page_3_spin_box_shift.setDisabled(False)
            self.ui.page_3_label_shift.setStyleSheet("color: white")
        else:
            self.ui.page_3_spin_box_shift.setDisabled(True)
            self.ui.page_3_label_shift.setStyleSheet("color: grey")

    def page_3_button_calc_clicked(self):
        processed_text = sym.polybius_square.make(
            text=self.ui.page_3_text_edit_input.toPlainText(),
            method=self.ui.page_3_combo_box_method.currentText(),
            shift=self.ui.page_3_spin_box_shift.value(),
            processing_type=self.ui.page_3_combo_box_type.currentText()
        )
        self.ui.page_3_text_edit_output.setText(processed_text)

    def page_4_button_calc_clicked(self):
        processed_text = sym.caesar.make(
            text=self.ui.page_4_text_edit_input.toPlainText(),
            shift=self.ui.page_4_spin_box_shift.value(),
            processing_type=self.ui.page_4_combo_box_type.currentText()
        )
        self.ui.page_4_text_edit_output.setText(processed_text)

    def page_5_button_gen_stencil_clicked(self):
        k = self.ui.page_5_spin_box_dim_stencil.value()
        stencil = sym.cardan_grille.gen_stencil(k)

        self.ui.page_5_table_widget_stencil.setRowCount(2*k)
        self.ui.page_5_table_widget_stencil.setColumnCount(2*k)

        for i in range(2*k):
            for j in range(2*k):
                item = QtWidgets.QTableWidgetItem(str(stencil[i, j].value))
                if stencil[i, j].cond:
                    item.setBackground(QtGui.QColor("orange"))
                self.ui.page_5_table_widget_stencil.setItem(i, j, item)

        self.ui.page_5_table_widget_stencil.resizeRowsToContents()
        self.ui.page_5_table_widget_stencil.resizeColumnsToContents()

    def page_5_button_calc_clicked(self):
        if self.ui.page_5_table_widget_stencil.rowCount() == 0:
            QtWidgets.QMessageBox.warning(self, "Warning!", "The stencil field is empty! Generate a stencil.")
            return

        self.ui.page_5_table_widget_preview.clear()
        n = self.ui.page_5_table_widget_stencil.rowCount()

        square = []
        for i in range(n):
            row = []
            for j in range(n):
                item = self.ui.page_5_table_widget_stencil.item(i, j)
                row.append(sym.cardan_grille.Field(int(item.text()), item.background() == QtGui.QColor("orange")))
            square.append(row)

        processed_text = sym.cardan_grille.make(
            text=self.ui.page_5_text_edit_input.toPlainText(),
            stencil=np.array(square),
            litter_type=self.ui.page_5_combo_box_trash.currentText(),
            processing_type=self.ui.page_5_combo_box_type.currentText()
        )
        self.ui.page_5_text_edit_output.setText(processed_text.rstrip())

        n_blocks = len(processed_text) // n**2

        self.ui.page_5_table_widget_preview.setColumnCount(n)
        self.ui.page_5_table_widget_preview.setRowCount(n*n_blocks + n_blocks)

        offset_i = 0
        row_labels = []
        for k in range(0, len(processed_text), n**2):
            substr = processed_text[0:n**2]

            for i in range(n):
                row_labels.append(str(i + 1))
                for j in range(n):
                    item = QtWidgets.QTableWidgetItem(substr[i*n + j])
                    self.ui.page_5_table_widget_preview.setItem(i + offset_i, j, item)

            row_labels.append("")
            offset_i += n + 1

        self.ui.page_5_table_widget_preview.setVerticalHeaderLabels(row_labels)

        self.ui.page_5_table_widget_preview.resizeRowsToContents()
        self.ui.page_5_table_widget_preview.resizeColumnsToContents()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("../resources/icon/cyber-security.png"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
