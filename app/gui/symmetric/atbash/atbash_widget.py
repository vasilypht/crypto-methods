# This module contains the implementation of the widget for working
# with the encryption algorithm "Cipher Atbash".
from PyQt6.QtWidgets import QMessageBox

from .atbash_ui import Ui_Atbash
from app.crypto.symmetric.atbash import (
    Atbash,
    AtbashError
)
from app.gui.widgets import BaseQWidget


class AtbashWidget(BaseQWidget):
    def __init__(self, *args, **kwargs):
        """AtbashWidget class constructor"""
        super(AtbashWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_Atbash()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Atbash"

        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self):
        """Method - a slot for processing a signal when a button is pressed."""
        cipher = Atbash()

        # Depending on which widget is active, select the appropriate action.
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher)

            case _:
                return

    def _tab_text_processing(self, cipher: Atbash):
        """Method for encryption on the text processing tab."""
        # Getting data from a form
        data = self.ui.text_edit_input.toPlainText()

        # We call the "make" method, and pass data to it.
        try:
            processed_text = cipher.make(data)

        except AtbashError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
