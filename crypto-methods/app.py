import sys
import re
import webbrowser

from PyQt6 import (
    QtWidgets,
    QtGui,
    QtCore
)
import yaml
import numpy as np

from gui.mainwindow import Ui_MainWindow
from methods.symmetric import (
    atbash,
    scytale,
    polybius_square,
    caesar,
    cardan_grille,
    richelieu,
    gronsfeld,
    vigenere,
    playfair
)

QtCore.QDir.addSearchPath("icons", "resources/icons")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__config = None

        # General settings
        self.setWindowTitle("Crypto methods")
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.tree_widget_list_apps.clicked.connect(self.tree_widget_item_clicked)
        self.ui.group_box_right.setTitle("Cryptographic methods")
        self.ui.stackedWidget.setCurrentIndex(0)

        # page 0
        self.ui.page_0_button_vk.setIcon(QtGui.QIcon("icons:icon-vk.png"))
        self.ui.page_0_button_vk.clicked.connect(lambda: webbrowser.open(f"https://{self.ui.page_0_button_vk.text()}"))

        self.ui.page_0_button_tg.setIcon(QtGui.QIcon("icons:icon-telegram.png"))
        self.ui.page_0_button_tg.clicked.connect(lambda: webbrowser.open(f"https://{self.ui.page_0_button_tg.text()}"))

        self.ui.page_0_button_github.setIcon(QtGui.QIcon("icons:icon-github.png"))
        self.ui.page_0_button_github.clicked.connect(lambda: webbrowser.open(f"https://{self.ui.page_0_button_github.text()}"))

        # page 1
        self.ui.page_1_button_make.clicked.connect(self.page_1_button_make_clicked)

        # page 2
        self.ui.page_2_check_box_columns.stateChanged.connect(self.page_2_check_box_check)
        self.ui.page_2_button_make.clicked.connect(self.page_2_button_make_clicked)

        # page 3
        self.ui.page_3_combo_box_method.currentIndexChanged.connect(self.page_3_combo_box_check)
        self.ui.page_3_button_make.clicked.connect(self.page_3_button_make_clicked)

        # page 4
        self.ui.page_4_button_make.clicked.connect(self.page_4_button_make_clicked)

        # page 5
        self.ui.page_5_button_gen_stencil.clicked.connect(self.page_5_button_gen_stencil_clicked)
        self.ui.page_5_button_make.clicked.connect(self.page_5_button_make_clicked)
        self.ui.page_5_table_widget_stencil.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(0))
        self.ui.page_5_table_widget_stencil.clicked.connect(self.page_5_table_widget_change)
        self.ui.page_5_button_clean_stencil.clicked.connect(self.page_5_button_clean_stencil)

        # page 6
        self.ui.page_6_line_edit_key.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"^[(),\d]*$"))
        )
        self.ui.page_6_button_make.clicked.connect(self.page_6_button_make_clicked)

        # page 7

        # page 8
        self.ui.page_8_line_edit_key.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"^\d*$"))
        )
        self.ui.page_8_button_make.clicked.connect(self.page_8_button_make_clicked)

        # page 9
        self.ui.page_9_line_edit_key.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"^[а-яА-ЯёЁa-zA-Z]*$"))
        )
        self.ui.page_9_button_make.clicked.connect(self.page_9_button_make_clicked)

        # page 10
        self.ui.page_10_line_edit_key.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"(^[а-яА-ЯёЁ]*$)|(^[a-zA-Z]*$)"))
        )
        self.ui.page_10_button_make.clicked.connect(self.page_10_button_make_clicked)

        self.load_config()
        self.init_tree_widget()

    def tree_widget_item_clicked(self) -> None:
        """(Slot) Method for switching widgets."""
        item = self.ui.tree_widget_list_apps.currentItem()
        parent = item.parent()

        try:
            path = f"./{parent.text(0)}/{item.text(0)}"
        except AttributeError:
            path = f"./{item.text(0)}"

        self.ui.group_box_right.setTitle(path)
        self.ui.stackedWidget.setCurrentIndex(self.__config["task id"].get(item.text(0), 0))

    def load_config(self) -> None:
        """Method for reading config."""
        try:
            with open("config.yaml", "r") as cfg:
                self.__config = yaml.safe_load(cfg)

        except IOError:
            QtWidgets.QMessageBox.critical(self, "Error!", "Failed to open config!")
            sys.exit(0)

    def init_tree_widget(self) -> None:
        """Method for initializing the list of program names."""
        items = []

        for key, values in self.__config["task names"].items():
            item = QtWidgets.QTreeWidgetItem((key,))
            item.setIcon(0, QtGui.QIcon("icons:icon-folder.png"))

            for value in values:
                child = QtWidgets.QTreeWidgetItem((value,))
                child.setIcon(0, QtGui.QIcon("icons:icon-doc.png"))
                item.addChild(child)

            items.append(item)

        self.ui.tree_widget_list_apps.insertTopLevelItems(0, items)

    def page_1_button_make_clicked(self) -> None:
        """Atbash | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = atbash.make(
                text=self.ui.page_1_text_edit_input.toPlainText()
            )
            self.ui.page_1_text_edit_output.setText(processed_text)

        except atbash.AtbashError as e:
            QtWidgets.QMessageBox.warning(self, "Warning!", e.args[0])

    def page_2_check_box_check(self) -> None:
        """Scytale | (Slot) Method for activating/deactivating a checkbox."""
        if self.ui.page_2_check_box_columns.isChecked():
            self.ui.page_2_spin_box_columns.setDisabled(False)
            self.ui.page_2_check_box_columns.setStyleSheet("color: white")
        else:
            self.ui.page_2_spin_box_columns.setDisabled(True)
            self.ui.page_2_check_box_columns.setStyleSheet("color: grey")

    def page_2_button_make_clicked(self) -> None:
        """Scytale | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = scytale.make(
                text=self.ui.page_2_text_edit_input.toPlainText(),
                n=self.ui.page_2_spin_box_rows.value(),
                m=self.ui.page_2_spin_box_columns.value(),
                auto_m=not self.ui.page_2_check_box_columns.isChecked(),
                mode=self.ui.page_2_combo_box_mode.currentText().lower()
            )
            self.ui.page_2_text_edit_output.setText(processed_text)

        except scytale.ScytaleError as e:
            QtWidgets.QMessageBox.warning(self, "Warning!", e.args[0])

    def page_3_combo_box_check(self) -> None:
        """Polybius square | (Slot) Method for activating/deactivating a spinbox."""
        if self.ui.page_3_combo_box_method.currentText() == "Method 3":
            self.ui.page_3_spin_box_shift.setDisabled(False)
            self.ui.page_3_label_shift.setStyleSheet("color: white")
        else:
            self.ui.page_3_spin_box_shift.setDisabled(True)
            self.ui.page_3_label_shift.setStyleSheet("color: grey")

    def page_3_button_make_clicked(self) -> None:
        """Polybius square | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = polybius_square.make(
                text=self.ui.page_3_text_edit_input.toPlainText(),
                shift=self.ui.page_3_spin_box_shift.value(),
                method=self.ui.page_3_combo_box_method.currentText().lower(),
                mode=self.ui.page_3_combo_box_mode.currentText().lower()
            )
            self.ui.page_3_text_edit_output.setText(processed_text)

        except polybius_square.PolybiusSquareError as e:
            QtWidgets.QMessageBox.warning(self, "Warning!", e.args[0])

    def page_4_button_make_clicked(self) -> None:
        """Caesar | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = caesar.make(
                text=self.ui.page_4_text_edit_input.toPlainText(),
                shift=self.ui.page_4_spin_box_shift.value(),
                mode=self.ui.page_4_combo_box_mode.currentText().lower()
            )
            self.ui.page_4_text_edit_output.setText(processed_text)

        except caesar.CaesarError as e:
            QtWidgets.QMessageBox.warning(self, "Warning!", e.args[0])

    def page_5_button_gen_stencil_clicked(self) -> None:
        """Cardan grille | (Slot) Method for creating a stencil on button click"""
        k = self.ui.page_5_spin_box_dim_stencil.value()
        stencil = cardan_grille.gen_stencil(k)

        self.ui.page_5_table_widget_stencil.setRowCount(2 * k)
        self.ui.page_5_table_widget_stencil.setColumnCount(2 * k)

        for i in range(2*k):
            for j in range(2*k):
                item = QtWidgets.QTableWidgetItem(str(stencil[i, j].value))
                if stencil[i, j].cond:
                    item.setBackground(QtGui.QColor("orange"))
                self.ui.page_5_table_widget_stencil.setItem(i, j, item)

        self.ui.page_5_table_widget_stencil.resizeRowsToContents()
        self.ui.page_5_table_widget_stencil.resizeColumnsToContents()

    def page_5_button_clean_stencil(self) -> None:
        """Cardan grille | (Slot) Method for creating a clean stencil on button click."""
        k = self.ui.page_5_spin_box_dim_stencil.value()
        stencil = cardan_grille.gen_stencil(k)

        self.ui.page_5_table_widget_stencil.setRowCount(2 * k)
        self.ui.page_5_table_widget_stencil.setColumnCount(2 * k)

        for i in range(2 * k):
            for j in range(2 * k):
                item = QtWidgets.QTableWidgetItem(str(stencil[i, j].value))
                self.ui.page_5_table_widget_stencil.setItem(i, j, item)

        self.ui.page_5_table_widget_stencil.resizeRowsToContents()
        self.ui.page_5_table_widget_stencil.resizeColumnsToContents()

    def page_5_table_widget_change(self) -> None:
        """Cardan grille | (Slot) Method to change table cell color when cell is clicked."""
        item = self.ui.page_5_table_widget_stencil.currentItem()
        if item.background() == QtGui.QColor("orange"):
            item.setBackground(QtGui.QColor(0, 0, 0, 0))
        else:
            item.setBackground(QtGui.QColor("orange"))

    def page_5_button_make_clicked(self) -> None:
        """Cardan grille | (Slot) Method for handling button click. (Encryption/decryption)"""

        # clear preview table
        self.ui.page_5_table_widget_preview.clear()

        # Creating and filling a stencil from a widget.
        n = self.ui.page_5_table_widget_stencil.rowCount()
        square = np.empty(shape=(n, n), dtype=cardan_grille.Field)

        for i in range(n):
            for j in range(n):
                item = self.ui.page_5_table_widget_stencil.item(i, j)
                square[i, j] = cardan_grille.Field(
                    int(item.text()),
                    item.background() == QtGui.QColor("orange")
                )

        try:
            processed_text = cardan_grille.make(
                text=self.ui.page_5_text_edit_input.toPlainText(),
                stencil=square,
                litter_type=self.ui.page_5_combo_box_trash.currentText().lower(),
                mode=self.ui.page_5_combo_box_mode.currentText().lower()
            )

        except cardan_grille.CarganGrilleError as e:
            QtWidgets.QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_5_text_edit_output.setText(processed_text)

        text_blocks = [processed_text[i:i+n**2] for i in range(0, len(processed_text), n**2)]

        self.ui.page_5_table_widget_preview.setColumnCount(n)
        self.ui.page_5_table_widget_preview.setRowCount(n * len(text_blocks) + len(text_blocks))

        # Output of processed text after stencil
        offset_i = 0
        row_labels = []
        for text_block in text_blocks:
            text_block += " " * (n**2 - len(text_block))

            for i in range(n):
                row_labels.append(str(i + 1))

                for j in range(n):
                    item = QtWidgets.QTableWidgetItem(text_block[i * n + j])
                    self.ui.page_5_table_widget_preview.setItem(i + offset_i, j, item)

            row_labels.append("")
            offset_i += n + 1

        self.ui.page_5_table_widget_preview.setVerticalHeaderLabels(row_labels)
        self.ui.page_5_table_widget_preview.resizeRowsToContents()
        self.ui.page_5_table_widget_preview.resizeColumnsToContents()

    def page_6_button_make_clicked(self) -> None:
        """Richelieu | (Slot) Method for handling button click. (Encryption/decryption)"""
        if not self.ui.page_6_text_edit_input.toPlainText():
            QtWidgets.QMessageBox.warning(self, "Warning!", "The field is empty. Enter something!")
            return

        key_text = self.ui.page_6_line_edit_key.text()
        input_text = self.ui.page_6_text_edit_input.toPlainText()

        if not key_text:
            QtWidgets.QMessageBox.warning(self, "Warning!", "The key field is empty. Enter the key!")
            return

        if not re.match(r"^\(\d+(,\d+|\)\(\d+)*\)$", key_text):
            QtWidgets.QMessageBox.warning(self, "Warning!", "Invalid key entered!")
            return

        # parse key str
        key_list = key_text.strip("()").split(")(")
        for i in range(len(key_list)):
            subkey = key_list[i].split(",")
            key_list[i] = list(map(int, subkey))

        # check range
        for subkey in key_list:
            for i in range(1, len(subkey) + 1):
                if i not in subkey:
                    QtWidgets.QMessageBox.warning(self, "Warning!", "Invalid key entered!")
                    return

        processed_text = richelieu.make(
            text=input_text,
            key=key_list,
            processing_type=self.ui.page_6_combo_box_mode.currentText().lower()
        )
        self.ui.page_6_text_edit_output.setText(processed_text)

    def page_8_button_make_clicked(self) -> None:
        """Gronsfeld | (Slot) Method for handling button click. (Encryption/decryption)"""
        if not self.ui.page_8_text_edit_input.toPlainText():
            QtWidgets.QMessageBox.warning(self, "Warning!", "The field is empty. Enter something!")
            return

        if not self.ui.page_8_line_edit_key.text():
            QtWidgets.QMessageBox.warning(self, "Warning!", "The key field is empty. Enter something!")
            return

        input_text = self.ui.page_8_text_edit_input.toPlainText()
        key_text = self.ui.page_8_line_edit_key.text()

        if not re.match(r"^\d*$", key_text):
            QtWidgets.QMessageBox.warning(self, "Warning!", "Invalid key entered!")
            return

        processed_text = gronsfeld.make(
            text=input_text,
            key=key_text,
            mode=self.ui.page_8_combo_box_mode.currentText().lower()
        )

        self.ui.page_8_text_edit_output.setText(processed_text)

    def page_9_button_make_clicked(self) -> None:
        """Vigenere | (Slot) Method for handling button click. (Encryption/decryption)"""
        if not self.ui.page_9_text_edit_input.toPlainText():
            QtWidgets.QMessageBox.warning(self, "Warning!", "The field is empty. Enter something!")
            return

        if not self.ui.page_9_line_edit_key.text():
            QtWidgets.QMessageBox.warning(self, "Warning!", "The key field is empty. Enter something!")
            return

        input_text = self.ui.page_9_text_edit_input.toPlainText()
        key_text = self.ui.page_9_line_edit_key.text()

        if not re.match(r"^[а-яА-ЯёЁa-zA-Z]*$", key_text):
            QtWidgets.QMessageBox.warning(self, "Warning!", "Invalid key entered!")
            return

        processed_text = vigenere.make(
            text=input_text,
            key=key_text,
            mode=self.ui.page_9_combo_box_mode.currentText().lower()
        )
        self.ui.page_9_text_edit_output.setText(processed_text)

    def page_10_button_make_clicked(self):
        """Playfair | (Slot) Method for handling button click. (Encryption/decryption)"""
        if not self.ui.page_10_text_edit_input.toPlainText():
            QtWidgets.QMessageBox.warning(self, "Warning!", "The field is empty. Enter something!")
            return

        if not self.ui.page_10_line_edit_key.text():
            QtWidgets.QMessageBox.warning(self, "Warning!", "The key field is empty. Enter something!")
            return

        input_text = self.ui.page_10_text_edit_input.toPlainText()
        key_text = self.ui.page_10_line_edit_key.text()

        if not re.match(r"(^[а-яА-ЯёЁ]*$)|(^[a-zA-Z]*$)", key_text):
            QtWidgets.QMessageBox.warning(self, "Warning!", "Invalid key entered!")
            return

        processed_text = playfair.make(
            text=input_text,
            key=key_text,
            mode=self.ui.page_10_combo_box_mode.currentText().lower()
        )
        self.ui.page_10_text_edit_output.setText(processed_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icons:icon-app.png"))
    app.setStyleSheet(open("gui/stylesheet.css").read())
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
