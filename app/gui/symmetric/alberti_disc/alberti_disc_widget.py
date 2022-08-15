from PyQt6.QtCore import (
    QRegularExpression as QRegExp
)
from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)
from PyQt6.QtGui import (
    QRegularExpressionValidator as QRegExpVal
)

from .alberti_disc_ui import Ui_AlbertiDisk
from app.crypto.symmetric.alberti_disc import (
    Alberti,
    AlbertiError
)


class AlbertiDiscWidget(QWidget):
    def __init__(self):
        super(AlbertiDiscWidget, self).__init__()
        self.ui = Ui_AlbertiDisk()
        self.ui.setupUi(self)

        self.title = "Alberti disc"

        self.ui.line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"(^[а-яё]*$)|(^[a-z]*$)", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Alberti disc | (Slot) Method for handling button click. (Encryption/decryption)"""
        key = self.ui.line_edit_key.text()
        step = self.ui.spin_box_iteration_step.value()
        shift = self.ui.spin_box_key_alphabet_shift.value()
        mode = self.ui.combo_box_mode.currentText().lower()

        try:
            cipher = Alberti(key, step, shift)

        except AlbertiError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case _:
                pass

    def _tab_text_processing(self, cipher: Alberti, mode: str):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except AlbertiError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
