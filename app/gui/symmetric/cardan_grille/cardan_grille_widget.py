from PyQt6.QtWidgets import (
    QMessageBox,
    QAbstractItemView,
    QTableWidgetItem,
    QMenu
)
from PyQt6.QtGui import QColor

from .cardan_grille_ui import Ui_CardanGrille
from app.crypto.symmetric.cardan_grille import (
    CarganGrille,
    CarganGrilleError
)
from app.gui.widgets import BaseQWidget


class CardanGrilleWidget(BaseQWidget):
    def __init__(self):
        super(CardanGrilleWidget, self).__init__()
        self.ui = Ui_CardanGrille()
        self.ui.setupUi(self)

        self.title = "Cardan grille"
        self.stencil = None

        self.ui.table_widget_stencil.setSelectionMode(QAbstractItemView.SelectionMode(0))

        self._action_gen_clean_stencil_clicked()

        # Context menu
        menu = QMenu()
        menu.addAction("Generate stencil", self._action_gen_stencil_clicked)
        menu.addAction("Generate clean stencil", self._action_gen_clean_stencil_clicked)
        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self._button_make_clicked)
        self.ui.table_widget_stencil.clicked.connect(self._table_widget_change)

    def _action_gen_stencil_clicked(self) -> None:
        """Cardan grille | (Slot) Method for creating a stencil on button click"""
        k = self.ui.spin_box_dim_stencil.value()
        self.stencil = CarganGrille.gen_stencil(k)

        self.ui.table_widget_stencil.setRowCount(2 * k)
        self.ui.table_widget_stencil.setColumnCount(2 * k)

        for i in range(2 * k):
            for j in range(2 * k):
                item = QTableWidgetItem(str(self.stencil[i, j].value))
                if self.stencil[i, j].cond:
                    item.setBackground(QColor("orange"))
                self.ui.table_widget_stencil.setItem(i, j, item)

        self.ui.table_widget_stencil.resizeRowsToContents()
        self.ui.table_widget_stencil.resizeColumnsToContents()

    def _action_gen_clean_stencil_clicked(self) -> None:
        """Cardan grille | (Slot) Method for creating a clean stencil on button click."""
        k = self.ui.spin_box_dim_stencil.value()
        self.stencil = CarganGrille.gen_stencil(k)

        self.ui.table_widget_stencil.setRowCount(2 * k)
        self.ui.table_widget_stencil.setColumnCount(2 * k)

        for i in range(2 * k):
            for j in range(2 * k):
                item = QTableWidgetItem(str(self.stencil[i, j].value))
                self.ui.table_widget_stencil.setItem(i, j, item)

        self.ui.table_widget_stencil.resizeRowsToContents()
        self.ui.table_widget_stencil.resizeColumnsToContents()

    def _table_widget_change(self) -> None:
        """Cardan grille | (Slot) Method to change table cell color when cell is clicked."""
        item = self.ui.table_widget_stencil.currentItem()
        i, j = item.row(), item.column()

        if item.background() == QColor("orange"):
            item.setBackground(QColor(0, 0, 0, 0))
            self.stencil[i][j].cond = False
        else:
            item.setBackground(QColor("orange"))
            self.stencil[i][j].cond = True

    def _button_make_clicked(self) -> None:
        """Cardan grille | (Slot) Method for handling button click. (Encryption/decryption)"""
        trash = self.ui.combo_box_trash.currentText().lower()
        mode = self.ui.combo_box_mode.currentText().lower()

        try:
            cipher = CarganGrille(self.stencil, trash)

        except CarganGrilleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case _:
                pass

    def _tab_text_processing(self, cipher: CarganGrille, mode: str):
        # clear preview table
        self.ui.table_widget_preview.clear()
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except CarganGrilleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
        n, _ = self.stencil.shape

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
