import string

from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)

from .hill_ui import Ui_Hill
from app.crypto.symmetric.hill import (
    Hill,
    HillError
)


class HillWidget(QWidget):
    def __init__(self):
        super(HillWidget, self).__init__()
        self.ui = Ui_Hill()
        self.ui.setupUi(self)

        self.title = "Hill"

        self.ui.line_edit_alphabet.setText(string.ascii_lowercase + "!?,")
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Hill | (Slot) Method for handling button click. (Encryption/decryption)"""
        key = self.ui.line_edit_key.text()
        alphabet = self.ui.line_edit_alphabet.text()
        mode = self.ui.combo_box_mode.currentText().lower()

        try:
            cipher = Hill(key, alphabet)

        except HillError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case _:
                pass

    def _tab_text_processing(self, cipher: Hill, mode: str):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except HillError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
