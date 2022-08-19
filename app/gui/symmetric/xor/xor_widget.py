from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout
)
from PyQt6.QtCore import QUrl

import numpy as np

from .xor_ui import Ui_XOR
from app.crypto.symmetric.xor import (
    XOR,
    XORError
)
from app.crypto.prngs.rc4 import (
    RC4,
    RC4Error
)
from app.crypto.common import EncProc
from app.gui.widgets import (
    DragDropWidget,
    PBarCommands,
    BaseQWidget,
    BaseQThread
)
from app.gui.const import (
    XOR_SUPPORT_EXT,
    MAX_BYTES_READ
)


class XORWidget(BaseQWidget):
    def __init__(self):
        super(XORWidget, self).__init__()
        self.ui = Ui_XOR()
        self.ui.setupUi(self)

        self.title = "XOR"

        self.file_path = QUrl()

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(XOR_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Context menu
        menu = QMenu()
        menu.addAction("Generate IV", self._action_gen_iv_clicked)
        menu.addSeparator()
        menu.addAction("Save IV", self._action_save_iv_clicked)
        menu.addAction("Load IV", self._action_load_iv_clicked)
        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _button_make_clicked(self) -> None:
        """XOR | (Slot) Method for handling button click. (Encryption/decryption)"""
        key = self.gen_xor_key()
        enc_proc = EncProc.from_str(self.ui.combo_box_mode.currentText())

        try:
            cipher = XOR(key)

        except XORError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case self.ui.tab_document:
                self._tab_document_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: XOR, enc_proc: EncProc):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_data = cipher.make(data, enc_proc)

        except XORError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_data)

    def _tab_document_processing(self, cipher: XOR, enc_proc: EncProc):
        if self.file_path.isEmpty():
            QMessageBox.warning(self, "Warning!", "File not selected!")
            return

        # get the name of the new file
        file_path_output, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save new file",
            directory="",
            filter=XOR_SUPPORT_EXT,
        )

        if not file_path_output:
            return

        thread_worker = FileProcessing(cipher, enc_proc, self.file_path.toLocalFile(), file_path_output)
        self.thread_ready.emit(thread_worker)

    def _action_gen_iv_clicked(self):
        iv = np.random.randint(0, 256, self.ui.spin_box_iv_size.value())
        iv_hex = bytes(tuple(iv)).hex()
        self.ui.line_edit_iv.setText(iv_hex)

    def _action_save_iv_clicked(self):
        if not self.ui.line_edit_iv.text():
            QMessageBox.warning(self, "Warning!", "The field with the IV is empty!")
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
                f_out.write(self.ui.line_edit_iv.text())

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

    def _action_load_iv_clicked(self):
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
                self.ui.line_edit_iv.setText(f_out.read())

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

    def gen_xor_key(self):
        try:
            rc4 = RC4(self.ui.line_edit_iv.text())
        except RC4Error as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        return bytes(next(rc4) for _ in range(self.ui.spin_box_gamma_size.value())).hex()

    def _file_path_changed(self, file: QUrl):
        self.file_path = file


class FileProcessing(BaseQThread):
    def __init__(self, cipher: XOR, enc_proc: EncProc, input_file: str, output_file: str):
        super(FileProcessing, self).__init__()
        self._cipher = cipher
        self._enc_proc = enc_proc
        self._input_file = input_file
        self._output_file = output_file

        self._is_worked = True

    def close(self):
        self._is_worked = False
        self.wait()

    def run(self) -> None:
        try:
            with open(self._input_file, "rb") as input_file, \
                    open(self._output_file, "wb") as output_file:
                input_file.seek(0, 2)
                input_file_size = input_file.tell()
                input_file.seek(0, 0)

                self.pbar.emit((PBarCommands.SET_RANGE, 0, input_file_size))
                self.pbar.emit((PBarCommands.SET_VALUE, 0))
                self.pbar.emit((PBarCommands.SHOW,))

                while (block := input_file.read(MAX_BYTES_READ)) and self._is_worked:
                    encrypted_block = self._cipher.make(block, self._enc_proc, reset_state=False)
                    output_file.write(encrypted_block)

                    self.pbar.emit((PBarCommands.SET_VALUE, input_file.tell()))

        except Exception as e:
            self.message.emit("An error occurred while working with files or when "
                              "determining the file size. (Check encryption mode)\n"
                              f"({e.args[0]})")

        finally:
            self.pbar.emit((PBarCommands.CLOSE,))
