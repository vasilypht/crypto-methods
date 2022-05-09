from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)

from .atbash_ui import Ui_atbash
from app.crypto.symmetric import atbash


class AtbashWidget(QWidget):
    def __init__(self):
        super(AtbashWidget, self).__init__()
        self.ui = Ui_atbash()
        self.ui.setupUi(self)

        self.title = "Atbash"

        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self):
        """Atbash | (Slot) Method for handling button click. (Encryption/decryption)"""
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                try:
                    processed_text = atbash.make(
                        text=self.ui.text_edit_input.toPlainText()
                    )

                except atbash.AtbashError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

                self.ui.text_edit_output.setText(processed_text)

            case _:
                return
