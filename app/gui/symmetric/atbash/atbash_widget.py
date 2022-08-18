from PyQt6.QtWidgets import QMessageBox

from .atbash_ui import Ui_Atbash
from app.crypto.symmetric.atbash import (
    Atbash,
    AtbashError
)
from app.gui.widgets import BaseQWidget


class AtbashWidget(BaseQWidget):
    def __init__(self):
        super(AtbashWidget, self).__init__()
        self.ui = Ui_Atbash()
        self.ui.setupUi(self)

        self.title = "Atbash"

        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self):
        """Atbash | (Slot) Method for handling button click. (Encryption/decryption)"""
        cipher = Atbash()

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher)

            case _:
                return

    def _tab_text_processing(self, cipher: Atbash):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data)

        except AtbashError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
