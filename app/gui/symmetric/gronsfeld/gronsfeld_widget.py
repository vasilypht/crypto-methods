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

from .gronsfeld_ui import Ui_Gronsfeld
from app.crypto.symmetric.gronsfeld import (
    Gronsfeld,
    GronsfeldError
)


class GronsfeldWidget(QWidget):
    def __init__(self):
        super(GronsfeldWidget, self).__init__()
        self.ui = Ui_Gronsfeld()
        self.ui.setupUi(self)

        self.title = "Gronsfeld"

        self.ui.line_edit_key.setValidator(QRegExpVal(QRegExp(r"^\d*$")))
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Gronsfeld | (Slot) Method for handling button click. (Encryption/decryption)"""
        key = self.ui.line_edit_key.text()
        mode = self.ui.combo_box_mode.currentText().lower()

        try:
            cipher = Gronsfeld(key)

        except GronsfeldError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case _:
                pass

    def _tab_text_processing(self, cipher: Gronsfeld, mode: str):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except GronsfeldError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
