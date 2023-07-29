# This module contains the implementation of the widget for working
# with the encryption algorithm "Caesar's cipher".
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QUrl

from .caesar_ui import Ui_Caesar
from app.crypto.symmetric import Caesar
from app.crypto.common import EncProc
from app.gui.widgets import (
    BaseQWidget
)


class CaesarWidget(BaseQWidget):
    def __init__(self):
        """CaesarWidget class constructor"""
        super(CaesarWidget, self).__init__()
        self.ui = Ui_Caesar()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Caesar"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        # Path received from dragdrop widget
        self.input_file_path = QUrl()

        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        # Getting data from a form
        shift = self.ui.spin_box_shift.value()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        cipher = Caesar(shift)

        # Depending on which widget is active, select the appropriate action.
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: Caesar, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        # Getting data from a form
        data = self.ui.text_edit_input.toPlainText()

        # We call the "make" method, and pass data and processing type to it.
        try:
            processed_text = cipher.make(data, enc_proc)

        except TypeError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)