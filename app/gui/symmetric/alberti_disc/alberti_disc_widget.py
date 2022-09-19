# This module contains the implementation of the widget for working
# with the encryption algorithm "Alberti's Disk".
from PyQt6.QtCore import QRegularExpression as QRegExp
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator as QRegExpVal

from .alberti_disc_ui import Ui_AlbertiDisk
from app.crypto.symmetric import Alberti
from app.crypto.common import EncProc
from app.gui.widgets import BaseQWidget


class AlbertiDiscWidget(BaseQWidget):
    def __init__(self, *args, **kwargs) -> None:
        """AlbertiDiscWidget class constructor"""
        super(AlbertiDiscWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_AlbertiDisk()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Alberti disc"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        # We set validation so that only Russian characters can be entered, or only English characters.
        self.ui.line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"(^[а-яё]*$)|(^[a-z]*$)", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        # Getting data from a form
        key = self.ui.line_edit_key.text()
        step = self.ui.spin_box_iteration_step.value()
        shift = self.ui.spin_box_key_alphabet_shift.value()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        # We create an object, if an exception occurs, then we display an
        # error message and exit the method.
        try:
            cipher = Alberti(key, step, shift)

        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        # Depending on which widget is active, select the appropriate action.
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: Alberti, enc_proc: EncProc) -> None:
        """Method for encryption on the text processing tab."""
        # Getting data from a form
        data = self.ui.text_edit_input.toPlainText()

        # We call the "make" method, and pass data and processing type to it.
        try:
            processed_text = cipher.make(data, enc_proc)

        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
