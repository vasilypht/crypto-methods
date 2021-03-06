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

from .gronsfeld_ui import Ui_gronsfeld
from app.crypto.symmetric import gronsfeld


class GronsfeldWidget(QWidget):
    def __init__(self):
        super(GronsfeldWidget, self).__init__()
        self.ui = Ui_gronsfeld()
        self.ui.setupUi(self)

        self.title = "Gronsfeld"

        self.ui.line_edit_key.setValidator(QRegExpVal(QRegExp(r"^\d*$")))
        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Gronsfeld | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = gronsfeld.make(
                text=self.ui.text_edit_input.toPlainText(),
                key=self.ui.line_edit_key.text(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except gronsfeld.GronsfeldError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
