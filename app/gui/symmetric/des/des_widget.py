# This module contains the implementation of the widget for working
# with the encryption algorithm "DES".
from random import randbytes
import json
from io import BytesIO
from typing import Literal, Optional

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
    QTextEdit,
)
from PyQt6.QtCore import QUrl

from .des_ui import Ui_DES
from app.crypto.symmetric import DES
from app.crypto.common import EncProc
from app.gui.const import ALL_SUPPORT_EXT
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget,
    BaseQThread,
    PBar,
)


class DESWidget(BaseQWidget):
    def __init__(self):
        """DESWidget class constructor"""
        super(DESWidget, self).__init__()
        self.ui = Ui_DES()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "DES"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))
        self.ui.combo_box_enc_mode.addItems((item.name for item in DES.EncMode))

        # Path received from dragdrop widget
        self.file_path = QUrl()

        # Create a dragdrop widget and place it on the document tab.
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(ALL_SUPPORT_EXT)
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

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _action_gen_iv_clicked(self):
        """Method for generating an initialization vector."""
        self.ui.line_edit_iv.setText(randbytes(8).hex())

    def _action_gen_key_clicked(self):
        """Method for generating a key."""
        self.ui.line_edit_key.setText(randbytes(7).hex())

    def _action_save_state_clicked(self):
        """Method for storing the key and initialization vector."""
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
            "mode": self.ui.combo_box_enc_mode.currentText(),
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
        """Method for loading the key and initialization vector."""
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

        self.ui.combo_box_enc_mode.setCurrentText(data.get("mode", "ECB"))
        self.ui.line_edit_iv.setText(data.get("iv", ""))
        self.ui.line_edit_key.setText(data.get("key", ""))

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        key_hex = self.ui.line_edit_key.text()
        iv_hex = self.ui.line_edit_iv.text()

        enc_mode = DES.EncMode.from_str(self.ui.combo_box_enc_mode.currentText())
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = DES(key_hex, iv_hex, enc_mode)

        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                cipher.set_reset_iv_flag(False)
                self.ui.text_edit_output.setText("")

                thread_worker = DataProcessing(
                    cipher=cipher,
                    enc_proc=enc_proc,
                    mode="string",
                    input_string=self.ui.text_edit_input.toPlainText(),
                    output_text_edit=self.ui.text_edit_output,
                )

            case self.ui.tab_document:
                cipher.set_reset_iv_flag(False)
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                # We get the path to the output file from the user.
                file_path_output, _ = QFileDialog.getSaveFileName(
                    parent=self,
                    caption="Save new file",
                    directory="",
                    filter=ALL_SUPPORT_EXT,
                )

                if not file_path_output:
                    return

                thread_worker = DataProcessing(
                    cipher=cipher,
                    enc_proc=enc_proc,
                    mode="file",
                    input_file_path=self.file_path.toLocalFile(),
                    output_file_path=file_path_output,
                )

            case _:
                assert False

        self.thread_ready.emit(thread_worker)

    def _tab_text_processing(self, cipher: DES, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_data = cipher.make(data, enc_proc)

        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_data)

    def _tab_document_processing(self, cipher: DES, enc_proc: EncProc):
        """Method for encryption on the document processing tab."""
        if self.file_path.isEmpty():
            QMessageBox.warning(self, "Warning!", "File not selected!")
            return

        # We get the path to the output file from the user.
        file_path_output, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save new file",
            directory="",
            filter=ALL_SUPPORT_EXT,
        )

        if not file_path_output:
            return

    def _file_path_changed(self, file: QUrl):
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file


class DataProcessing(BaseQThread):
    def __init__(
            self,
            cipher: DES,
            *,
            output_text_edit: Optional[QTextEdit] = None,
            input_string: str = "",
            input_file_path: Optional[str] = None,
            output_file_path: Optional[str] = None,
            mode: Literal["file", "string"] = "string",
            enc_proc: EncProc = EncProc.ENCRYPT,
            **options
    ) -> None:
        super(DataProcessing, self).__init__()

        self._cipher = cipher
        self._output_text_edit = output_text_edit
        self._input_string = input_string
        self._input_file_path = input_file_path
        self._output_file_path = output_file_path
        self._mode = mode
        self._enc_proc = enc_proc

        self._read_block_size = options.get("read_block_size", 4096)

        self._is_worked = True

    def close(self) -> None:
        self._is_worked = False
        self.wait()

    def run(self) -> None:
        output_buffer = BytesIO()

        match self._mode, self._enc_proc:
            case "file", _:
                try:
                    input_buffer = open(self._input_file_path, "rb")
                    output_buffer = open(self._output_file_path, "wb")
                except IOError:
                    self.message.emit((
                        BaseQThread.MessageType.WARNING,
                        "Warning!",
                        "Error opening file!",
                    ))
                    return

            case "string", EncProc.ENCRYPT:
                input_buffer = BytesIO(self._input_string.encode("utf-8"))

            case "string", EncProc.DECRYPT:
                input_buffer = BytesIO(bytes.fromhex(self._input_string))

        try:
            input_buffer.seek(0, 2)
            input_buffer_size = input_buffer.tell()
            input_buffer.seek(0, 0)

            self.pbar.emit((PBar.Commands.SET_RANGE, 0, input_buffer_size))
            self.pbar.emit((PBar.Commands.SET_VALUE, 0))
            self.pbar.emit((PBar.Commands.SHOW,))

            match self._enc_proc:
                case EncProc.ENCRYPT:
                    pad = input_buffer_size.to_bytes(8, "little")
                    encrypted_pad = self._cipher.encrypt(pad)
                    output_buffer.write(encrypted_pad)

                case EncProc.DECRYPT:
                    pad = input_buffer.read(8)
                    decrypted_pad = self._cipher.decrypt(pad)
                    final_file_size = int.from_bytes(decrypted_pad, "little")

                case _:
                    return

            while (block := input_buffer.read(self._read_block_size)) and self._is_worked:
                processed_block = self._cipher.make(block, self._enc_proc)
                output_buffer.write(processed_block)

                self.pbar.emit((PBar.Commands.SET_VALUE, input_buffer.tell()))

            if self._enc_proc is EncProc.DECRYPT:
                output_buffer.truncate(final_file_size)

            if self._mode == "string":
                match self._enc_proc:
                    case EncProc.ENCRYPT:
                        self._output_text_edit.append(output_buffer.getvalue().hex())

                    case EncProc.DECRYPT:
                        self._output_text_edit.append(output_buffer.getvalue().decode("utf-8"))

                    case _:
                        assert False

        except Exception as e:
            self.message.emit((
                BaseQThread.MessageType.CRITICAL,
                "Unknown error!",
                "An error occurred while working with file or when determining the file size.\n"
                f"({e.args[0]})"
            ))

        finally:
            input_buffer.close()
            output_buffer.close()
            self.pbar.emit((PBar.Commands.CLOSE,))

