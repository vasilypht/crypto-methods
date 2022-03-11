from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)

from src.modules.caesar.caesar_ui import Ui_caesar
from src.crypto.symmetric import caesar


class CaesarWidget(QWidget):
    def __init__(self):
        super(CaesarWidget, self).__init__()
        self.ui = Ui_caesar()
        self.ui.setupUi(self)

        self.title = "Caesar"

        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Caesar | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = caesar.make(
                text=self.ui.text_edit_input.toPlainText(),
                shift=self.ui.spin_box_shift.value(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except caesar.CaesarError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
