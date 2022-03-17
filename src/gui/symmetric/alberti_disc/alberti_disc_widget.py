from PyQt6.QtCore import (
    QRegularExpression as QRegExp,
    Qt
)
from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QStyledItemDelegate
)
from PyQt6.QtGui import (
    QRegularExpressionValidator as QRegExpVal
)

from .alberti_disc_ui import Ui_alberti_disc
from src.crypto.symmetric import alberti_disc


class AlbertiDiscWidget(QWidget):
    def __init__(self):
        super(AlbertiDiscWidget, self).__init__()
        self.ui = Ui_alberti_disc()
        self.ui.setupUi(self)

        self.title = "Alberti disc"

        self.ui.combo_box_mode.setItemDelegate(QStyledItemDelegate())
        self.ui.combo_box_mode.view().window().setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.ui.combo_box_mode.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ui.line_edit_key.setValidator(
            QRegExpVal(QRegExp(r"(^[а-яё]*$)|(^[a-z]*$)", QRegExp.PatternOption.CaseInsensitiveOption))
        )
        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Alberti disc | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = alberti_disc.make(
                text=self.ui.text_edit_input.toPlainText(),
                key=self.ui.line_edit_key.text(),
                step=self.ui.spin_box_iteration_step.value(),
                shift=self.ui.spin_box_key_alphabet_shift.value(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except alberti_disc.AlbertiError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
