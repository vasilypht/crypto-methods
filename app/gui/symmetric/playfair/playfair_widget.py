from PyQt6.QtCore import QRegularExpression as QRegExp
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator as QRegExpVal

from .playfair_ui import Ui_Playfair
from app.crypto.symmetric.playfair import (
    Playfair,
    PlayfairError
)
from app.crypto.common import EncProc
from app.gui.widgets import BaseQWidget


class PlayfairWidget(BaseQWidget):
    def __init__(self):
        super(PlayfairWidget, self).__init__()
        self.ui = Ui_Playfair()
        self.ui.setupUi(self)

        self.title = "Playfair"

        self.ui.line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"(^[а-яё]*$)|(^[a-z]*$)", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Playfair | (Slot) Method for handling button click. (Encryption/decryption)"""
        key = self.ui.line_edit_key.text()
        enc_proc = EncProc.from_str(self.ui.combo_box_mode.currentText())

        try:
            cipher = Playfair(key)

        except PlayfairError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: Playfair, enc_proc: EncProc):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, enc_proc)

        except PlayfairError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
