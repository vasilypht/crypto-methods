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

from .richelieu_ui import Ui_Richelieu
from app.crypto.symmetric.richelieu import (
    Richelieu,
    RichelieuError
)


class RichelieuWidget(QWidget):
    def __init__(self):
        super(RichelieuWidget, self).__init__()
        self.ui = Ui_Richelieu()
        self.ui.setupUi(self)

        self.title = "Richelieu"

        self.ui.line_edit_key.setValidator(QRegExpVal(QRegExp(r"^[(),\d]*$")))
        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Richelieu | (Slot) Method for handling button click. (Encryption/decryption)"""
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing()

            case _:
                pass

    def _tab_text_processing(self):
        try:
            cipher = Richelieu(self.ui.line_edit_key.text())

            processed_text = cipher.make(
                text=self.ui.text_edit_input.toPlainText(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except RichelieuError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
