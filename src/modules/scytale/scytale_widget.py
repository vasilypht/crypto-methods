from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)

from src.modules.scytale.scytale_ui import Ui_scytale
from src.crypto.symmetric import scytale


class ScytaleWidget(QWidget):
    def __init__(self):
        super(ScytaleWidget, self).__init__()
        self.ui = Ui_scytale()
        self.ui.setupUi(self)

        self.title = "Scytale"

        self.ui.check_box_columns.stateChanged.connect(self.check_box_check)
        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def check_box_check(self) -> None:
        """Scytale | (Slot) Method for activating/deactivating a checkbox."""
        if self.ui.check_box_columns.isChecked():
            self.ui.spin_box_columns.setDisabled(False)
            self.ui.check_box_columns.setStyleSheet("color: white")
        else:
            self.ui.spin_box_columns.setDisabled(True)
            self.ui.check_box_columns.setStyleSheet("color: grey")

    def button_make_clicked(self) -> None:
        """Scytale | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = scytale.make(
                text=self.ui.text_edit_input.toPlainText(),
                n=self.ui.spin_box_rows.value(),
                m=self.ui.spin_box_columns.value(),
                auto_m=not self.ui.check_box_columns.isChecked(),
                mode=self.ui.combo_box_mode.currentText().lower()
            )

        except scytale.ScytaleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
