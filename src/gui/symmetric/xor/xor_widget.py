from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
)
from PyQt6.QtCore import (
    QUrl,
    QThread,
    pyqtSignal,
)

import numpy as np

from .xor_ui import Ui_XOR
from src.gui.widgets import DragDropWidget, PBar
from src.gui.const import (
    XOR_SUPPORT_EXT,
    MAX_BYTES_READ
)
from src.crypto.symmetric.xor import (
    XOR,
    XORError
)
from src.crypto.prngs.rc4 import (
    RC4,
    RC4Error
)


class XORWidget(QWidget):
    def __init__(self):
        super(XORWidget, self).__init__()
        self.ui = Ui_XOR()
        self.ui.setupUi(self)

        self.title = "XOR"

        self.file_path = QUrl()

        self.pbar = PBar()
        self.file_worker_thread = FileProcessing(self)
        self.file_worker_thread.update_pbar.connect(self.pbar.signal_handler)
        self.file_worker_thread.message.connect(lambda m: QMessageBox.warning(self, "Warning!", m))
        self.pbar.close_clicked.connect(lambda: self.file_worker_thread.close())

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(XOR_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Context menu
        menu = QMenu()
        menu.addAction("Generate IV", self.action_gen_iv_clicked)
        menu.addSeparator()
        menu.addAction("Save IV", self.action_save_iv_clicked)
        menu.addAction("Load IV", self.action_load_iv_clicked)
        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self.button_make_clicked)

        self.drag_drop_widget.dropped.connect(self.file_path_changed)
        self.drag_drop_widget.canceled.connect(self.file_path_changed)

    def button_make_clicked(self) -> None:
        """XOR | (Slot) Method for handling button click. (Encryption/decryption)"""
        iv_hex = self.ui.line_edit_iv.text()
        try:
            rc4 = RC4(iv=iv_hex)
        except RC4Error as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        key = bytes(next(rc4) for _ in range(self.ui.spin_box_gamma_size.value())).hex()
        xor = XOR(key)

        mode = self.ui.combo_box_mode.currentText().lower()
        data = self.ui.text_edit_input.toPlainText()

        match self.ui.tab_widget.currentWidget():

            case self.ui.tab_text:
                try:
                    match mode:
                        case "encrypt":
                            processed_data = xor.encrypt(data)

                        case "decrypt":
                            processed_data = xor.decrypt(data)

                        case _:
                            raise XORError(f"Wrong encryption mode! ({mode})")

                except XORError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

                self.ui.text_edit_output.setText(processed_data)

            case self.ui.tab_document:
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

                self.file_worker_thread.set_options(
                    cipher=xor,
                    mode=mode,
                    input_file=self.file_path.toLocalFile(),
                    output_file=file_path_output
                )
                self.file_worker_thread.start()

    def action_gen_iv_clicked(self):
        iv = np.random.randint(0, 256, self.ui.spin_box_iv_size.value())
        iv_hex = bytes(tuple(iv)).hex()
        self.ui.line_edit_iv.setText(iv_hex)

    def action_save_iv_clicked(self):
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

    def action_load_iv_clicked(self):
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

    def file_path_changed(self, file: QUrl):
        self.file_path = file


class FileProcessing(QThread):
    update_pbar = pyqtSignal(tuple)
    message = pyqtSignal(str)

    def __init__(self, parent):
        super(FileProcessing, self).__init__(parent)
        self.cipher = None
        self.mode = None
        self.input_file = None
        self.output_file = None

        self._is_worked = True

    def set_options(self, cipher: XOR, mode: str, input_file: str, output_file: str):
        self.cipher = cipher
        self.mode = mode
        self.input_file = input_file
        self.output_file = output_file

    def close(self):
        self._is_worked = False
        self.wait()

    def run(self) -> None:
        self._is_worked = True

        try:
            with open(self.input_file, "rb") as input_file, \
                    open(self.output_file, "wb") as output_file:
                input_file.seek(0, 2)
                input_file_size = input_file.tell()
                input_file.seek(0, 0)

                self.update_pbar.emit(("range", 0, input_file_size))
                self.update_pbar.emit(("show",))

                while (block := input_file.read(MAX_BYTES_READ)) and self._is_worked:
                    encrypted_block = self.cipher.make(block, self.mode, reset_state=False)
                    output_file.write(encrypted_block)
                    self.update_pbar.emit(("current_value", input_file.tell()))

                self.update_pbar.emit(("close",))

        except Exception as e:
            self.update_pbar.emit(("close",))
            self.message.emit("An error occurred while working with files or when "
                              "determining the file size. (Check encryption mode)\n"
                              f"({e.args[0]})")
            return
