from random import randbytes
import json

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
)
from PyQt6.QtCore import QUrl

from .des_ui import Ui_DES
from app.crypto.symmetric.des import (
    DES,
    DESError,
    EncMode
)
from app.crypto.common import EncProc
from app.gui.const import (
    DES_SUPPORT_EXT,
    MAX_BYTES_READ
)
from app.gui.widgets import (
    DragDropWidget,
    BaseQThread,
    BaseQWidget,
    PBarCommands
)


class DESWidget(BaseQWidget):
    def __init__(self):
        super(DESWidget, self).__init__()
        self.ui = Ui_DES()
        self.ui.setupUi(self)

        self.title = "DES"

        self.file_path = QUrl()

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(DES_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Context menu
        menu = QMenu()
        menu.addAction("Generate IV", self._action_gen_iv_clicked)
        menu.addAction("Generate key", self._action_gen_key_clicked)
        menu.addSeparator()
        menu.addAction("Save state", self._action_save_state_clicked)
        menu.addAction("Load state", self._action_load_state_clicked)
        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _action_gen_iv_clicked(self):
        self.ui.line_edit_iv.setText(randbytes(8).hex())

    def _action_gen_key_clicked(self):
        self.ui.line_edit_key.setText(randbytes(7).hex())

    def _action_save_state_clicked(self):
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

    def _action_load_state_clicked(self):
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

    def _button_make_clicked(self) -> None:
        """DES | (Slot) Method for handling button click. (Encryption/decryption)"""
        key_hex = self.ui.line_edit_key.text()
        iv_hex = self.ui.line_edit_iv.text()

        enc_mode = EncMode.from_str(self.ui.combo_box_des_mode.currentText())
        enc_proc = EncProc.from_str(self.ui.combo_box_mode.currentText())

        try:
            cipher = DES(key_hex, iv_hex, enc_mode)

        except DESError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case self.ui.tab_document:
                self._tab_document_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: DES, enc_proc: EncProc):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_data = cipher.make(data, enc_proc)

        except DESError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_data)

    def _tab_document_processing(self, cipher: DES, enc_proc: EncProc):
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

        thread_worker = FileProcessing(cipher, enc_proc, self.file_path.toLocalFile(), file_path_output)
        self.thread_ready.emit(thread_worker)

    def _file_path_changed(self, file: QUrl):
        self.file_path = file


class FileProcessing(BaseQThread):
    def __init__(self, cipher: DES, enc_proc: EncProc, input_file: str, output_file: str):
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

                match self._enc_proc:
                    case EncProc.ENCRYPT:
                        # padding to 8 bytes
                        pad = input_file_size.to_bytes(8, "little")
                        encrypted_pad = self._cipher.encrypt(pad, reset_iv=False)
                        output_file.write(encrypted_pad)

                    case EncProc.DECRYPT:
                        pad = input_file.read(8)
                        decrypted_pad = self._cipher.decrypt(pad, reset_iv=False)
                        final_file_size = int.from_bytes(decrypted_pad, "little")

                    case _:
                        return

                while (block := input_file.read(MAX_BYTES_READ)) and self._is_worked:
                    processed_block = self._cipher.make(block, self._enc_proc, reset_iv=False)
                    output_file.write(processed_block)

                    self.pbar.emit((PBarCommands.SET_VALUE, input_file.tell()))

                if self._enc_proc is EncProc.DECRYPT:
                    output_file.truncate(final_file_size)

        except Exception as e:
            self.message.emit("An error occurred while working with files or when "
                              "determining the file size. (Check encryption mode)\n"
                              f"({e.args[0]})")

        finally:
            self.pbar.emit((PBarCommands.CLOSE,))
