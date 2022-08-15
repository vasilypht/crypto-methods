from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox
)

from .polybius_square_ui import Ui_PolybiusSquare
from app.crypto.symmetric.polybius_square import (
    PolybiusSquareError,
    PolybiusSquare
)


class PolybiusSquareWidget(QWidget):
    def __init__(self):
        super(PolybiusSquareWidget, self).__init__()
        self.ui = Ui_PolybiusSquare()
        self.ui.setupUi(self)

        self.title = "Polybius square"

        self.ui.combo_box_method.currentIndexChanged.connect(self._combo_box_check)
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _combo_box_check(self) -> None:
        """Polybius square | (Slot) Method for activating/deactivating a spinbox."""
        if self.ui.combo_box_method.currentText() == "Method 2":
            self.ui.spin_box_shift.setDisabled(False)
            self.ui.label_shift.setDisabled(False)
        else:
            self.ui.spin_box_shift.setDisabled(True)
            self.ui.label_shift.setDisabled(True)

    def _button_make_clicked(self) -> None:
        """Polybius square | (Slot) Method for handling button click. (Encryption/decryption)"""
        shift = self.ui.spin_box_shift.value()
        method = self.ui.combo_box_method.currentText().lower()
        mode = self.ui.combo_box_mode.currentText().lower()

        try:
            cipher = PolybiusSquare(shift, method)

        except PolybiusSquareError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case _:
                pass

    def _tab_text_processing(self, cipher: PolybiusSquare, mode: str):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except PolybiusSquareError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)

