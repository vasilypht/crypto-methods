from random import randbytes
import json

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
    Qt
)

from .des_ui import Ui_DES
from app.gui.widgets import DragDropWidget, PBar
from app.gui.const import (
    DES_SUPPORT_EXT,
    MAX_BYTES_READ
)
from app.crypto.symmetric.des import (
    DES,
    DESError
)


class DESWidget(QWidget):
    def __init__(self):
        super(DESWidget, self).__init__()
        self.ui = Ui_DES()
        self.ui.setupUi(self)

        self.title = "DES"

        self.file_path = QUrl()

        self.pbar = PBar()
        self.pbar.setWindowTitle(self.title)
        self.pbar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.file_worker_thread = FileProcessing(self)
        self.file_worker_thread.update_pbar.connect(self.pbar.signal_handler)
        self.file_worker_thread.message.connect(lambda m: QMessageBox.warning(self, "Warning!", m))
        self.pbar.close_clicked.connect(lambda: self.file_worker_thread.close())

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(DES_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Context menu
        menu = QMenu()
        menu.addAction("Generate IV", self.action_gen_iv_clicked)
        menu.addAction("Generate key", self.action_gen_key_clicked)
        menu.addSeparator()
        menu.addAction("Save state", self.action_save_state_clicked)
        menu.addAction("Load state", self.action_load_state_clicked)
        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self.button_make_clicked)

        self.drag_drop_widget.dropped.connect(self.file_path_changed)
        self.drag_drop_widget.canceled.connect(self.file_path_changed)

    def action_gen_iv_clicked(self):
        self.ui.line_edit_iv.setText(randbytes(8).hex())

    def action_gen_key_clicked(self):
        self.ui.line_edit_key.setText(randbytes(7).hex())

    def action_save_state_clicked(self):
        if not self.ui.line_edit_iv.text():
            QMessageBox.warning(self, "Warning!", "The field with the IV is empty!")
            return

        if not self.ui.line_edit_key.text():
            QMessageBox.warning(self, "Warning!", "The field with the key is empty!")
            return

        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save a state file",
            directory="",
            filter="All files (*)",
            initialFilter="All files (*)"
        )

        if not filename:
            return

        data = {
            "mode": self.ui.combo_box_des_mode.currentText(),
            "iv": self.ui.line_edit_iv.text(),
            "key": self.ui.line_edit_key.text()
        }

        try:
            with open(filename, "w") as f_out:
                f_out.write(json.dumps(data))

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

    def action_load_state_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a state file",
            directory="",
            filter="All files (*)",
            initialFilter="All files (*)"
        )

        if not filename:
            return

        try:
            with open(filename, "r") as f_in:
                data = json.loads(f_in.read())

        except json.JSONDecodeError:
            QMessageBox.warning(self, "Warning!", "Error reading data, check the correctness of the data!")
            return

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

        self.ui.combo_box_des_mode.setCurrentText(data.get("mode", "ECB"))
        self.ui.line_edit_iv.setText(data.get("iv", ""))
        self.ui.line_edit_key.setText(data.get("key", ""))

    def button_make_clicked(self) -> None:
        """DES | (Slot) Method for handling button click. (Encryption/decryption)"""
        key_hex = self.ui.line_edit_key.text()
        iv_hex = self.ui.line_edit_iv.text()
        des_mode = self.ui.combo_box_des_mode.currentText()
        des = DES(key=key_hex, iv=iv_hex, mode=des_mode)

        mode = self.ui.combo_box_mode.currentText().lower()

        match self.ui.tab_widget.currentWidget():

            case self.ui.tab_text:
                data = self.ui.text_edit_input.toPlainText()

                try:
                    processed_data = des.make(data, mode)

                except DESError as e:
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
                    filter=DES_SUPPORT_EXT,
                )

                if not file_path_output:
                    return

                self.file_worker_thread.set_options(
                    cipher=des,
                    mode=mode,
                    input_file=self.file_path.toLocalFile(),
                    output_file=file_path_output
                )
                self.file_worker_thread.start()

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

    def set_options(self, cipher: DES, mode: str, input_file: str, output_file: str):
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

                if self.mode == "encrypt":
                    # padding to 8 bytes
                    pad = input_file_size.to_bytes(8, "little")
                    encrypted_pad = self.cipher.encrypt(pad)
                    output_file.write(encrypted_pad)

                if self.mode == "decrypt":
                    pad = input_file.read(8)
                    decrypted_pad = self.cipher.decrypt(pad)
                    final_file_size = int.from_bytes(decrypted_pad, "little")

                while (block := input_file.read(MAX_BYTES_READ)) and self._is_worked:
                    processed_block = self.cipher.make(block, self.mode)
                    output_file.write(processed_block)
                    self.update_pbar.emit(("current_value", input_file.tell()))

                if self.mode == "decrypt":
                    output_file.truncate(final_file_size)

                self.update_pbar.emit(("close",))

        except Exception as e:
            self.update_pbar.emit(("close",))
            self.message.emit("An error occurred while working with files or when "
                              "determining the file size. (Check encryption mode)\n"
                              f"({e.args[0]})")
            return
