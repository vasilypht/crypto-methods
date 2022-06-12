from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)

from .atbash_ui import Ui_Atbash
from app.crypto.symmetric.atbash import (
    Atbash,
    AtbashError
)


class AtbashWidget(QWidget):
    def __init__(self):
        super(AtbashWidget, self).__init__()
        self.ui = Ui_Atbash()
        self.ui.setupUi(self)

        self.title = "Atbash"

        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self):
        """Atbash | (Slot) Method for handling button click. (Encryption/decryption)"""
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing()

            case _:
                return

    def _tab_text_processing(self):
        cipher = Atbash()

        try:
            processed_text = cipher.make(
                text=self.ui.text_edit_input.toPlainText()
            )

        except AtbashError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
