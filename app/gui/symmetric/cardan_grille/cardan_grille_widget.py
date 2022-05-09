from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QAbstractItemView,
    QTableWidgetItem
)
from PyQt6.QtGui import (
    QColor
)
import numpy as np

from .cardan_grille_ui import Ui_cardan_grille
from app.crypto.symmetric import cardan_grille


class CardanGrilleWidget(QWidget):
    def __init__(self):
        super(CardanGrilleWidget, self).__init__()
        self.ui = Ui_cardan_grille()
        self.ui.setupUi(self)

        self.title = "Cardan grille"

        self.ui.table_widget_stencil.setSelectionMode(QAbstractItemView.SelectionMode(0))

        self.ui.button_gen_stencil.clicked.connect(self.button_gen_stencil_clicked)
        self.ui.button_make.clicked.connect(self.button_make_clicked)
        self.ui.table_widget_stencil.clicked.connect(self.table_widget_change)
        self.ui.button_clean_stencil.clicked.connect(self.button_clean_stencil)

    def button_gen_stencil_clicked(self) -> None:
        """Cardan grille | (Slot) Method for creating a stencil on button click"""
        k = self.ui.spin_box_dim_stencil.value()
        stencil = cardan_grille.gen_stencil(k)

        self.ui.table_widget_stencil.setRowCount(2 * k)
        self.ui.table_widget_stencil.setColumnCount(2 * k)

        for i in range(2 * k):
            for j in range(2 * k):
                item = QTableWidgetItem(str(stencil[i, j].value))
                if stencil[i, j].cond:
                    item.setBackground(QColor("orange"))
                self.ui.table_widget_stencil.setItem(i, j, item)

        self.ui.table_widget_stencil.resizeRowsToContents()
        self.ui.table_widget_stencil.resizeColumnsToContents()

    def button_clean_stencil(self) -> None:
        """Cardan grille | (Slot) Method for creating a clean stencil on button click."""
        k = self.ui.spin_box_dim_stencil.value()
        stencil = cardan_grille.gen_stencil(k)

        self.ui.table_widget_stencil.setRowCount(2 * k)
        self.ui.table_widget_stencil.setColumnCount(2 * k)

        for i in range(2 * k):
            for j in range(2 * k):
                item = QTableWidgetItem(str(stencil[i, j].value))
                self.ui.table_widget_stencil.setItem(i, j, item)

        self.ui.table_widget_stencil.resizeRowsToContents()
        self.ui.table_widget_stencil.resizeColumnsToContents()

    def table_widget_change(self) -> None:
        """Cardan grille | (Slot) Method to change table cell color when cell is clicked."""
        item = self.ui.table_widget_stencil.currentItem()
        if item.background() == QColor("orange"):
            item.setBackground(QColor(0, 0, 0, 0))
        else:
            item.setBackground(QColor("orange"))

    def button_make_clicked(self) -> None:
        """Cardan grille | (Slot) Method for handling button click. (Encryption/decryption)"""

        # clear preview table
        self.ui.table_widget_preview.clear()

        # Creating and filling a stencil from a widget.
        n = self.ui.table_widget_stencil.rowCount()
        square = np.empty(shape=(n, n), dtype=cardan_grille.Field)

        for i in range(n):
            for j in range(n):
                item = self.ui.table_widget_stencil.item(i, j)
                square[i, j] = cardan_grille.Field(
                    int(item.text()),
                    item.background() == QColor("orange")
                )

        try:
            processed_text = cardan_grille.make(
                text=self.ui.text_edit_input.toPlainText(),
                stencil=square,
                litter_type=self.ui.combo_box_trash.currentText().lower(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except cardan_grille.CarganGrilleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)

        text_blocks = [processed_text[i:i + n ** 2] for i in range(0, len(processed_text), n ** 2)]

        self.ui.table_widget_preview.setColumnCount(n)
        self.ui.table_widget_preview.setRowCount(n * len(text_blocks) + len(text_blocks))

        # Output of processed text after stencil
        offset_i = 0
        row_labels = []
        for text_block in text_blocks:
            text_block += " " * (n ** 2 - len(text_block))

            for i in range(n):
                row_labels.append(str(i + 1))

                for j in range(n):
                    item = QTableWidgetItem(text_block[i * n + j])
                    self.ui.table_widget_preview.setItem(i + offset_i, j, item)

            row_labels.append("")
            offset_i += n + 1

        self.ui.table_widget_preview.setVerticalHeaderLabels(row_labels)
        self.ui.table_widget_preview.resizeRowsToContents()
        self.ui.table_widget_preview.resizeColumnsToContents()
