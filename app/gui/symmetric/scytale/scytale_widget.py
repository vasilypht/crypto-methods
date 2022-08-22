# This module contains the implementation of the widget for working
# with the encryption algorithm "Scytale cipher".
from PyQt6.QtWidgets import QMessageBox

from .scytale_ui import Ui_Scytale
from app.crypto.symmetric.scytale import Scytale
from app.crypto.exceptions import ScytaleError
from app.crypto.common import EncProc
from app.gui.widgets import BaseQWidget


class ScytaleWidget(BaseQWidget):
    def __init__(self):
        """ScytaleWidget class constructor"""
        super(ScytaleWidget, self).__init__()
        self.ui = Ui_Scytale()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Scytale"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        self.ui.check_box_columns.stateChanged.connect(self._check_box_check)
        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _check_box_check(self) -> None:
        """Method for activating/deactivating a checkbox."""
        if self.ui.check_box_columns.isChecked():
            self.ui.spin_box_columns.setDisabled(False)
            self.ui.check_box_columns.setStyleSheet("color: palette(window-text)")
        else:
            self.ui.spin_box_columns.setDisabled(True)
            self.ui.check_box_columns.setStyleSheet("color: grey")

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        n = self.ui.spin_box_rows.value()
        m = self.ui.spin_box_columns.value()
        auto_m = not self.ui.check_box_columns.isChecked()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = Scytale(n, m, auto_m)

        except ScytaleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                return

    def _tab_text_processing(self, cipher: Scytale, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, enc_proc)

        except ScytaleError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
