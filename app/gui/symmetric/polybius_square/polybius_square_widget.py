# This module contains the implementation of the widget for working
# with the encryption algorithm "Polybius Square".
from PyQt6.QtWidgets import (
    QMessageBox
)

from .polybius_square_ui import Ui_PolybiusSquare
from app.gui.widgets import BaseQWidget
from app.crypto.symmetric import PolybiusSquare
from app.crypto.exceptions import PolybiusSquareError
from app.crypto.common import EncProc


class PolybiusSquareWidget(BaseQWidget):
    def __init__(self):
        """PolybiusSquareWidget class constructor"""
        super(PolybiusSquareWidget, self).__init__()
        self.ui = Ui_PolybiusSquare()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Polybius square"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))
        self.ui.combo_box_method_mode.addItems(
            (item.name.replace("_", " ").capitalize() for item in PolybiusSquare.MethodMode))

        self.ui.combo_box_method_mode.currentIndexChanged.connect(self._combo_box_check)
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _combo_box_check(self) -> None:
        """Method for activating/deactivating a spinbox."""
        if self.ui.combo_box_method_mode.currentText() == "Method 2":
            self.ui.spin_box_shift.setDisabled(False)
            self.ui.label_shift.setDisabled(False)
        else:
            self.ui.spin_box_shift.setDisabled(True)
            self.ui.label_shift.setDisabled(True)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        shift = self.ui.spin_box_shift.value()
        method_mode = PolybiusSquare.MethodMode.from_str(self.ui.combo_box_method_mode.currentText())
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = PolybiusSquare(shift, method_mode)

        except PolybiusSquareError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: PolybiusSquare, enc_proc: EncProc) -> None:
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, enc_proc)

        except PolybiusSquareError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
