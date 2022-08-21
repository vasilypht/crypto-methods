# This module contains the implementation of the widget for working
# with the encryption algorithm "Vernam".
from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog
)

from .vernam_ui import Ui_vernam
from app.crypto.symmetric.vernam import (
    Vernam,
    VernamError
)
from app.crypto.common import EncProc
from app.gui.widgets import BaseQWidget


class VernamWidget(BaseQWidget):
    def __init__(self):
        super(VernamWidget, self).__init__()
        self.ui = Ui_vernam()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Vernam"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        self.ui.button_make.clicked.connect(self._button_make_clicked)

        # Context menu
        menu = QMenu()
        menu.addAction("Generate key", self._action_clicked_gen_key)
        menu.addSeparator()
        menu.addAction("Save key", self._action_clicked_save_key)
        menu.addAction("Load key", self._action_clicked_load_key)
        self.ui.button_options.setMenu(menu)

    def _action_clicked_gen_key(self):
        """Method for generating a key."""
        if not self.ui.text_edit_input.toPlainText():
            QMessageBox.warning(self, "Warning!", "Input text field is empty!")
            return

        key_hex = Vernam.gen_key(len(self.ui.text_edit_input.toPlainText().encode("utf-8")))
        self.ui.line_edit_key.setText(key_hex)

    def _action_clicked_save_key(self):
        """Method for storing the key."""
        if not self.ui.line_edit_key.text():
            QMessageBox.warning(self, "Warning!", "The field with the key is empty!")
            return

        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save a key file",
            directory="",
            filter="Text File (*.txt)",
            initialFilter="Text File (*.txt)"
        )

        if not filename:
            return

        try:
            with open(filename, "w") as f_out:
                f_out.write(self.ui.line_edit_key.text())

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

    def _action_clicked_load_key(self):
        """Method for loading the key."""
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a key file",
            directory="",
            filter="Text File (*.txt)",
            initialFilter="Text File (*.txt)"
        )

        if not filename:
            return

        try:
            with open(filename, "r") as f_out:
                self.ui.line_edit_key.setText(f_out.read())

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        key = self.ui.line_edit_key.text()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = Vernam(key)

        except VernamError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: Vernam, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, enc_proc)

        except VernamError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
