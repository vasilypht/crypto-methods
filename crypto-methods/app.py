import sys
import webbrowser
import string

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QAbstractItemView,
    QMessageBox,
    QTreeWidgetItem,
    QTableWidgetItem
)
from PyQt6.QtGui import (
    QRegularExpressionValidator as QRegExpVal,
    QIcon,
    QColor
)
from PyQt6.QtCore import (
    QRegularExpression as QRegExp,
    QDir
)
import yaml
import numpy as np

from gui.mainwindow import Ui_MainWindow
from methods.symmetric import (
    atbash,
    scytale,
    polybius,
    caesar,
    cardano,
    richelieu,
    gronsfeld,
    vigenere,
    playfair,
    alberti,
    hill,
    vernam
)

QDir.addSearchPath("icons", "resources/icons")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.config = {}

        self.load_config()
        self.init_tree_widget()

        # General settings
        self.setWindowTitle(self.config.get("app name", "Crypto methods"))
        self.ui.stackedWidget.setCurrentIndex(self.config["task id"].get("Default", 0))
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.tree_widget_list_apps.clicked.connect(self.tree_widget_item_clicked)
        self.ui.group_box_right.setTitle("Cryptographic methods")

        # page 0 - Default
        self.ui.page_0_button_vk.setIcon(QIcon("icons:icon-vk.png"))
        self.ui.page_0_button_vk.clicked.connect(
            lambda: webbrowser.open(f"https://{self.ui.page_0_button_vk.text()}")
        )

        self.ui.page_0_button_tg.setIcon(QIcon("icons:icon-telegram.png"))
        self.ui.page_0_button_tg.clicked.connect(
            lambda: webbrowser.open(f"https://{self.ui.page_0_button_tg.text()}")
        )

        self.ui.page_0_button_github.setIcon(QIcon("icons:icon-github.png"))
        self.ui.page_0_button_github.clicked.connect(
            lambda: webbrowser.open(f"https://{self.ui.page_0_button_github.text()}")
        )

        # page 1 - Atbash
        self.ui.page_1_button_make.clicked.connect(self.page_1_button_make_clicked)

        # page 2 - Scytale
        self.ui.page_2_check_box_columns.stateChanged.connect(self.page_2_check_box_check)
        self.ui.page_2_button_make.clicked.connect(self.page_2_button_make_clicked)

        # page 3 - Polybius Square
        self.ui.page_3_combo_box_method.currentIndexChanged.connect(self.page_3_combo_box_check)
        self.ui.page_3_button_make.clicked.connect(self.page_3_button_make_clicked)

        # page 4 - Caesar
        self.ui.page_4_button_make.clicked.connect(self.page_4_button_make_clicked)

        # page 5 - Cardan grille
        self.ui.page_5_button_gen_stencil.clicked.connect(self.page_5_button_gen_stencil_clicked)
        self.ui.page_5_button_make.clicked.connect(self.page_5_button_make_clicked)
        self.ui.page_5_table_widget_stencil.setSelectionMode(QAbstractItemView.SelectionMode(0))
        self.ui.page_5_table_widget_stencil.clicked.connect(self.page_5_table_widget_change)
        self.ui.page_5_button_clean_stencil.clicked.connect(self.page_5_button_clean_stencil)

        # page 6 - Richelieu
        self.ui.page_6_line_edit_key.setValidator(QRegExpVal(QRegExp(r"^[(),\d]*$")))
        self.ui.page_6_button_make.clicked.connect(self.page_6_button_make_clicked)

        # page 7 - Alberti disc
        self.ui.page_7_line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"(^[а-яё]*$)|(^[a-z]*$)", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.page_7_button_make.clicked.connect(self.page_7_button_make_clicked)

        # page 8 - Gronsfeld
        self.ui.page_8_line_edit_key.setValidator(QRegExpVal(QRegExp(r"^\d*$")))
        self.ui.page_8_button_make.clicked.connect(self.page_8_button_make_clicked)

        # page 9 - Vigenere
        self.ui.page_9_line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"^[а-яёa-z]*$", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.page_9_button_make.clicked.connect(self.page_9_button_make_clicked)

        # page 10 - Playfair
        self.ui.page_10_line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"(^[а-яё]*$)|(^[a-z]*$)", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.page_10_button_make.clicked.connect(self.page_10_button_make_clicked)

        # page 11 - Hill
        self.ui.page_11_line_edit_alphabet.setText(string.ascii_lowercase + "!?,")
        self.ui.page_11_button_make.clicked.connect(self.page_11_button_make_clicked)

        # page 12 - Vernam
        self.ui.page_12_button_make.clicked.connect(self.page_12_button_make_clicked)

    def load_config(self) -> None:
        """Method for reading config."""
        try:
            with open("config.yaml", "r") as cfg:
                self.config = yaml.safe_load(cfg)

        except OSError:
            QMessageBox.critical(self, "Error!", "Failed to open or read file.")
            sys.exit(1)

    def init_tree_widget(self) -> None:
        """Method for initializing the list of program names."""
        def fill_item(parent: QTreeWidgetItem, data):
            match data:
                case list():
                    for value in data:
                        fill_item(parent, value)

                case dict():
                    for key, value in data.items():
                        child = QTreeWidgetItem((str(key),))
                        child.setIcon(0, QIcon("icons:icon-folder.png"))
                        parent.addChild(child)
                        fill_item(child, value)

                case _:
                    child = QTreeWidgetItem((str(data),))
                    child.setIcon(0, QIcon("icons:icon-doc.png"))
                    parent.addChild(child)

        self.ui.tree_widget_list_apps.clear()
        try:
            fill_item(self.ui.tree_widget_list_apps.invisibleRootItem(), self.config["task names"])

        except KeyError:
            QMessageBox.critical(self, "Error!", "Error reading config!\n"
                                                 "Check key 'task names'!")
            sys.exit(1)

    def tree_widget_item_clicked(self) -> None:
        """(Slot) Method for switching widgets."""
        current_item = self.ui.tree_widget_list_apps.currentItem()

        try:
            widget_index = self.config["task id"].get(
                current_item.text(0), self.config["task id"].get("Default", 0)
            )
            self.ui.stackedWidget.setCurrentIndex(widget_index)
            self.ui.group_box_right.setTitle(current_item.text(0))

        except KeyError:
            QMessageBox.critical(self, "Error!", "Error reading config!\n"
                                                 "Check key 'task id'!")
            sys.exit(1)

    def page_1_button_make_clicked(self) -> None:
        """Atbash | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = atbash.make(
                text=self.ui.page_1_text_edit_input.toPlainText()
            )
            self.ui.page_1_text_edit_output.setText(processed_text)

        except atbash.AtbashError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])

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

        except scytale.ScytaleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_2_text_edit_output.setText(processed_text)

    def page_3_combo_box_check(self) -> None:
        """Polybius square | (Slot) Method for activating/deactivating a spinbox."""
        if self.ui.page_3_combo_box_method.currentText() == "Method 2":
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

        except polybius_square.PolybiusSquareError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_3_text_edit_output.setText(processed_text)

    def page_4_button_make_clicked(self) -> None:
        """Caesar | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = caesar.make(
                text=self.ui.page_4_text_edit_input.toPlainText(),
                shift=self.ui.page_4_spin_box_shift.value(),
                mode=self.ui.page_4_combo_box_mode.currentText().lower()
            )

        except caesar.CaesarError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_4_text_edit_output.setText(processed_text)

    def page_5_button_gen_stencil_clicked(self) -> None:
        """Cardan grille | (Slot) Method for creating a stencil on button click"""
        k = self.ui.page_5_spin_box_dim_stencil.value()
        stencil = cardan_grille.gen_stencil(k)

        self.ui.page_5_table_widget_stencil.setRowCount(2 * k)
        self.ui.page_5_table_widget_stencil.setColumnCount(2 * k)

        for i in range(2*k):
            for j in range(2*k):
                item = QTableWidgetItem(str(stencil[i, j].value))
                if stencil[i, j].cond:
                    item.setBackground(QColor("orange"))
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
                item = QTableWidgetItem(str(stencil[i, j].value))
                self.ui.page_5_table_widget_stencil.setItem(i, j, item)

        self.ui.page_5_table_widget_stencil.resizeRowsToContents()
        self.ui.page_5_table_widget_stencil.resizeColumnsToContents()

    def page_5_table_widget_change(self) -> None:
        """Cardan grille | (Slot) Method to change table cell color when cell is clicked."""
        item = self.ui.page_5_table_widget_stencil.currentItem()
        if item.background() == QColor("orange"):
            item.setBackground(QColor(0, 0, 0, 0))
        else:
            item.setBackground(QColor("orange"))

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
                    item.background() == QColor("orange")
                )

        try:
            processed_text = cardan_grille.make(
                text=self.ui.page_5_text_edit_input.toPlainText(),
                stencil=square,
                litter_type=self.ui.page_5_combo_box_trash.currentText().lower(),
                mode=self.ui.page_5_combo_box_mode.currentText().lower()
            )

        except cardan_grille.CarganGrilleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
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
                    item = QTableWidgetItem(text_block[i * n + j])
                    self.ui.page_5_table_widget_preview.setItem(i + offset_i, j, item)

            row_labels.append("")
            offset_i += n + 1

        self.ui.page_5_table_widget_preview.setVerticalHeaderLabels(row_labels)
        self.ui.page_5_table_widget_preview.resizeRowsToContents()
        self.ui.page_5_table_widget_preview.resizeColumnsToContents()

    def page_6_button_make_clicked(self) -> None:
        """Richelieu | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = richelieu.make(
                text=self.ui.page_6_text_edit_input.toPlainText(),
                key=self.ui.page_6_line_edit_key.text(),
                mode=self.ui.page_6_combo_box_mode.currentText().lower()
            )

        except richelieu.RichelieuError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_6_text_edit_output.setText(processed_text)

    def page_7_button_make_clicked(self) -> None:
        """Alberti disc | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = alberti_disc.make(
                text=self.ui.page_7_text_edit_input.toPlainText(),
                key=self.ui.page_7_line_edit_key.text(),
                step=self.ui.page_7_spin_box_iteration_step.value(),
                shift=self.ui.page_7_spin_box_key_alphabet_shift.value(),
                mode=self.ui.page_7_combo_box_mode.currentText().lower()
            )

        except alberti_disc.AlbertiError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_7_text_edit_output.setText(processed_text)

    def page_8_button_make_clicked(self) -> None:
        """Gronsfeld | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = gronsfeld.make(
                text=self.ui.page_8_text_edit_input.toPlainText(),
                key=self.ui.page_8_line_edit_key.text(),
                mode=self.ui.page_8_combo_box_mode.currentText().lower()
            )

        except gronsfeld.GronsfeldError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_8_text_edit_output.setText(processed_text)

    def page_9_button_make_clicked(self) -> None:
        """Vigenere | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = vigenere.make(
                text=self.ui.page_9_text_edit_input.toPlainText(),
                key=self.ui.page_9_line_edit_key.text(),
                mode=self.ui.page_9_combo_box_mode.currentText().lower()
            )

        except vigenere.VigenereError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_9_text_edit_output.setText(processed_text)

    def page_10_button_make_clicked(self) -> None:
        """Playfair | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = playfair.make(
                text=self.ui.page_10_text_edit_input.toPlainText(),
                key=self.ui.page_10_line_edit_key.text(),
                mode=self.ui.page_10_combo_box_mode.currentText().lower()
            )

        except playfair.PlayfairError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_10_text_edit_output.setText(processed_text)

    def page_11_button_make_clicked(self) -> None:
        """Hill | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = hill.make(
                text=self.ui.page_11_text_edit_input.toPlainText(),
                key=self.ui.page_11_line_edit_key.text(),
                alphabet=self.ui.page_11_line_edit_alphabet.text(),
                mode=self.ui.page_11_combo_box_mode.currentText().lower()
            )

        except hill.HillError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_11_text_edit_output.setText(processed_text)

    def page_12_button_make_clicked(self) -> None:
        """Vernam | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = vernam.make(
                text=self.ui.page_12_text_edit_input.toPlainText(),
                key=self.ui.page_12_line_edit_key.text()
            )

        except vernam.VernamError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.page_12_text_edit_output.setText(processed_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons:icon-app.png"))
    app.setStyleSheet(open("gui/stylesheet.css").read())
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
