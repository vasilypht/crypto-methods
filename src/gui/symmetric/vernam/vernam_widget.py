from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)

from .vernam_ui import Ui_vernam
from src.crypto.symmetric import vernam


class VernamWidget(QWidget):
    def __init__(self):
        super(VernamWidget, self).__init__()
        self.ui = Ui_vernam()
        self.ui.setupUi(self)

        self.title = "Vernam"

        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Vernam | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = vernam.make(
                text=self.ui.text_edit_input.toPlainText(),
                key=self.ui.line_edit_key.text()
            )

        except vernam.VernamError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
