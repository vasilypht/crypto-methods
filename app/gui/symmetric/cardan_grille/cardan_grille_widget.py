# This module contains the implementation of the widget for working
# with the encryption algorithm "Grille Cardano".
from PyQt6.QtWidgets import (
    QMessageBox,
    QAbstractItemView,
    QTableWidgetItem,
    QMenu
)
from PyQt6.QtGui import QColor

from .cardan_grille_ui import Ui_CardanGrille
from app.crypto.symmetric import CarganGrille
from app.crypto.exceptions import CarganGrilleError
from app.crypto.common import EncProc
from app.gui.widgets import BaseQWidget


EncMode = CarganGrille.EncMode


class CardanGrilleWidget(BaseQWidget):
    def __init__(self):
        """CardanGrilleWidget class constructor"""
        super(CardanGrilleWidget, self).__init__()
        self.ui = Ui_CardanGrille()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Cardan grille"
        self.stencil = None

        # Initialization of possible encryption processes/modes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))
        self.ui.combo_box_enc_mode.addItems((item.name.replace("_", " ").capitalize() for item in EncMode))

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
        """Method for generating a stencil."""
        k = self.ui.spin_box_dim_stencil.value()
        self.stencil = CarganGrille.gen_stencil(k)

        # Adjusting the size of the table widget.
        self.ui.table_widget_stencil.setRowCount(2 * k)
        self.ui.table_widget_stencil.setColumnCount(2 * k)

        for i in range(2 * k):
            for j in range(2 * k):
                # We fill in the fields of the widget, if the value is marked,
                # then we paint the cell in orange
                item = QTableWidgetItem(str(self.stencil[i, j].value))

                if self.stencil[i, j].cond:
                    item.setBackground(QColor("orange"))

                self.ui.table_widget_stencil.setItem(i, j, item)

        # Fitting the Widget to the Data
        self.ui.table_widget_stencil.resizeRowsToContents()
        self.ui.table_widget_stencil.resizeColumnsToContents()

    def _action_gen_clean_stencil_clicked(self) -> None:
        """Method for generating a clean stencil."""
        k = self.ui.spin_box_dim_stencil.value()
        self.stencil = CarganGrille.gen_stencil(k)

        # Adjusting the size of the table widget.
        self.ui.table_widget_stencil.setRowCount(2 * k)
        self.ui.table_widget_stencil.setColumnCount(2 * k)

        for i in range(2 * k):
            for j in range(2 * k):
                item = QTableWidgetItem(str(self.stencil[i, j].value))
                self.ui.table_widget_stencil.setItem(i, j, item)

        # Fitting the Widget to the Data
        self.ui.table_widget_stencil.resizeRowsToContents()
        self.ui.table_widget_stencil.resizeColumnsToContents()

    def _table_widget_change(self) -> None:
        """Method - a slot for processing a signal on clicking on an element of the stencil widget."""
        # Get the indexes of the current item.
        item = self.ui.table_widget_stencil.currentItem()
        i, j = item.row(), item.column()

        # If the field has been checked, uncheck it and paint the field in the widget
        # in the normal color. Otherwise, paint orange and mark the field.
        if item.background() == QColor("orange"):
            item.setBackground(QColor(0, 0, 0, 0))
            self.stencil[i][j].cond = False
        else:
            item.setBackground(QColor("orange"))
            self.stencil[i][j].cond = True

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        enc_mode = EncMode.from_str(self.ui.combo_box_enc_mode.currentText())
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = CarganGrille(self.stencil, enc_mode)

        except CarganGrilleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: CarganGrille, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        # clear preview table
        self.ui.table_widget_preview.clear()

        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, enc_proc)

        except CarganGrilleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)

        # We divide the received text into blocks.
        n, _ = self.stencil.shape
        text_blocks = [processed_text[i:i + n ** 2] for i in range(0, len(processed_text), n ** 2)]

        # Set the size of the widget depending on the number of blocks.
        self.ui.table_widget_preview.setColumnCount(n)
        self.ui.table_widget_preview.setRowCount(n * len(text_blocks) + len(text_blocks))

        # Output of processed text after stencil
        # The value relative to which the square will be filled.
        offset_i = 0
        row_labels = []
        for text_block in text_blocks:
            # We add an empty string so that there is a distance between the
            # encrypted squares in the widget.
            text_block += " " * (n ** 2 - len(text_block))

            for i in range(n):
                row_labels.append(str(i + 1))

                for j in range(n):
                    item = QTableWidgetItem(text_block[i * n + j])
                    self.ui.table_widget_preview.setItem(i + offset_i, j, item)

            row_labels.append("")
            offset_i += n + 1

        # Fitting the Widget to the Data
        self.ui.table_widget_preview.setVerticalHeaderLabels(row_labels)
        self.ui.table_widget_preview.resizeRowsToContents()
        self.ui.table_widget_preview.resizeColumnsToContents()
