from PyQt6.QtWidgets import QMessageBox

from .scytale_ui import Ui_Scytale
from app.crypto.symmetric.scytale import (
    Scytale,
    ScytaleError
)
from app.gui.widgets import BaseQWidget


class ScytaleWidget(BaseQWidget):
    def __init__(self):
        super(ScytaleWidget, self).__init__()
        self.ui = Ui_Scytale()
        self.ui.setupUi(self)

        self.title = "Scytale"

        self.ui.check_box_columns.stateChanged.connect(self._check_box_check)
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _check_box_check(self) -> None:
        """Scytale | (Slot) Method for activating/deactivating a checkbox."""
        if self.ui.check_box_columns.isChecked():
            self.ui.spin_box_columns.setDisabled(False)
            self.ui.check_box_columns.setStyleSheet("color: palette(window-text)")
        else:
            self.ui.spin_box_columns.setDisabled(True)
            self.ui.check_box_columns.setStyleSheet("color: grey")

    def _button_make_clicked(self) -> None:
        """Scytale | (Slot) Method for handling button click. (Encryption/decryption)"""
        n = self.ui.spin_box_rows.value()
        m = self.ui.spin_box_columns.value()
        auto_m = not self.ui.check_box_columns.isChecked()
        mode = self.ui.combo_box_mode.currentText().lower()

        try:
            cipher = Scytale(n, m, auto_m)

        except ScytaleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case _:
                return

    def _tab_text_processing(self, cipher: Scytale, mode: str):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except ScytaleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
