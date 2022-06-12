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
        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Alberti disc | (Slot) Method for handling button click. (Encryption/decryption)"""
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing()

            case _:
                pass

    def _tab_text_processing(self):
        try:
            cipher = Alberti(
                key=self.ui.line_edit_key.text(),
                step=self.ui.spin_box_iteration_step.value(),
                shift=self.ui.spin_box_key_alphabet_shift.value()
            )

            processed_text = cipher.make(
                text=self.ui.text_edit_input.toPlainText(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except AlbertiError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
