# This module contains the implementation of the widget for working
# with the encryption algorithm "Hill cipher".
import string

from PyQt6.QtWidgets import QMessageBox

from .hill_ui import Ui_Hill
from app.crypto.symmetric.hill import Hill
from app.crypto.exceptions import HillError
from app.crypto.common import EncProc
from app.gui.widgets import BaseQWidget


class HillWidget(BaseQWidget):
    def __init__(self) -> None:
        """HillWidget class constructor"""
        super(HillWidget, self).__init__()
        self.ui = Ui_Hill()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Hill"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        # Initialization of alphabet.
        self.ui.line_edit_alphabet.setText(string.ascii_lowercase + "!?,")

        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        key = self.ui.line_edit_key.text()
        alphabet = self.ui.line_edit_alphabet.text()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = Hill(key, alphabet)

        except HillError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: Hill, enc_proc: EncProc) -> None:
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, enc_proc)

        except HillError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
