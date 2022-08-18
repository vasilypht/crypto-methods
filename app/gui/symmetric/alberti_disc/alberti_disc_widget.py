from PyQt6.QtCore import QRegularExpression as QRegExp
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator as QRegExpVal

from .alberti_disc_ui import Ui_AlbertiDisk
from app.crypto.symmetric.alberti_disc import (
    Alberti,
    AlbertiError
)
from app.gui.widgets import BaseQWidget


class AlbertiDiscWidget(BaseQWidget):
    def __init__(self) -> None:
        super(AlbertiDiscWidget, self).__init__()
        self.ui = Ui_AlbertiDisk()
        self.ui.setupUi(self)

        self.title = "Alberti disc"

        # We set validation so that only Russian characters can be entered, or only English characters.
        self.ui.line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"(^[а-яё]*$)|(^[a-z]*$)", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """(Slot) Method for handling button click. (Encryption/decryption)"""
        # Getting data from a form
        key = self.ui.line_edit_key.text()
        step = self.ui.spin_box_iteration_step.value()
        shift = self.ui.spin_box_key_alphabet_shift.value()
        mode = self.ui.combo_box_mode.currentText().lower()

        # We create an object, if an exception occurs, then we display an
        # error message and exit the method.
        try:
            cipher = Alberti(key, step, shift)

        except AlbertiError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        # Depending on which widget is active, select the appropriate action.
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case _:
                pass

    def _tab_text_processing(self, cipher: Alberti, mode: str) -> None:
        """"""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except AlbertiError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
