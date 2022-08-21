# This module contains the implementation of the widget for working
# with the encryption algorithm "Gronsfeld cipher".
from PyQt6.QtCore import QRegularExpression as QRegExp
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator as QRegExpVal

from .gronsfeld_ui import Ui_Gronsfeld
from app.crypto.symmetric.gronsfeld import (
    Gronsfeld,
    GronsfeldError
)
from app.crypto.common import EncProc
from app.gui.widgets import BaseQWidget


class GronsfeldWidget(BaseQWidget):
    def __init__(self):
        """GronsfeldWidget class constructor"""
        super(GronsfeldWidget, self).__init__()
        self.ui = Ui_Gronsfeld()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Gronsfeld"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        # Set validation on the key input widget.
        self.ui.line_edit_key.setValidator(QRegExpVal(QRegExp(r"^\d*$")))
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        key = self.ui.line_edit_key.text()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = Gronsfeld(key)

        except GronsfeldError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: Gronsfeld, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, enc_proc)

        except GronsfeldError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
