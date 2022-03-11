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

from src.modules.vigenere.vigenere_ui import Ui_vigenere
from src.crypto.symmetric import vigenere


class VigenereWidget(QWidget):
    def __init__(self):
        super(VigenereWidget, self).__init__()
        self.ui = Ui_vigenere()
        self.ui.setupUi(self)

        self.title = "Vigenere"

        self.ui.line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"^[а-яёa-z]*$", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Vigenere | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = vigenere.make(
                text=self.ui.text_edit_input.toPlainText(),
                key=self.ui.line_edit_key.text(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except vigenere.VigenereError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
