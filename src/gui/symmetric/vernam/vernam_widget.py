from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QMenu,
    QFileDialog
)
from PyQt6.QtCore import (
    Qt
)
import numpy as np

from .vernam_ui import Ui_vernam
from src.crypto.symmetric import vernam

MAX_BYTES_READ = 1024


class VernamWidget(QWidget):
    def __init__(self):
        super(VernamWidget, self).__init__()
        self.ui = Ui_vernam()
        self.ui.setupUi(self)
        self.title = "Vernam"

        self.ui.button_make.clicked.connect(self.button_make_clicked)

        # Context menu
        menu = QMenu()
        menu.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        menu.addAction("Generate key", self.action_clicked_gen_key)
        menu.addSeparator()
        menu.addAction("Save key", self.action_clicked_save_key)
        menu.addAction("Load key", self.action_clicked_load_key)
        self.ui.button_settings.setMenu(menu)

    def action_clicked_gen_key(self):
        if not self.ui.text_edit_input.toPlainText():
            QMessageBox.warning(self, "Warning!", "Input text field is empty!")
            return

        sample_bytes = np.random.randint(0, 256, len(self.ui.text_edit_input.toPlainText()))
        key_bytes = bytes(list(sample_bytes))
        self.ui.line_edit_key.setText(key_bytes.decode(encoding="KOI8-r"))

    def action_clicked_save_key(self):
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

        try:
            with open(filename, "w") as f_out:
                f_out.write(self.ui.line_edit_key.text())

        except OSError as e:
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

    def action_clicked_load_key(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a key file",
            directory="",
            filter="Text File (*.txt)",
            initialFilter="Text File (*.txt)"
        )

        try:
            with open(filename, "r") as f_out:
                self.ui.line_edit_key.setText(f_out.read(MAX_BYTES_READ))

        except OSError as e:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

    def button_make_clicked(self) -> None:
        """Vernam | (Slot) Method for handling button click. (Encryption/decryption)"""
        try:
            processed_text = vernam.make(
                text=self.ui.text_edit_input.toPlainText(),
                key=self.ui.line_edit_key.text()
            )

        except vernam.VernamError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)
