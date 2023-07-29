# This module contains the implementation of the widget for working
# with the encryption algorithm "XOR".
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

import numpy as np

from .xor_ui import Ui_XOR
from app.crypto.symmetric import XOR
from app.crypto.prngs import RC4
from app.crypto.common import EncProc
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget,
    BaseQThread,
    PBar,
)
from app.gui.const import XOR_SUPPORT_EXT


class XORWidget(BaseQWidget):
    def __init__(self):
        """XORWidget class constructor"""
        super(XORWidget, self).__init__()
        self.ui = Ui_XOR()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "XOR"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        # Path received from dragdrop widget
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

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        key = self.gen_xor_key()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = XOR(key)

        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                cipher.set_reset_state_flag(False)
                self.ui.text_edit_output.setText("")

                thread_worker = DataProcessing(
                    cipher=cipher,
                    input_string=self.ui.text_edit_input.toPlainText(),
                    output_text_edit=self.ui.text_edit_output,
                    mode="string",
                    enc_proc=enc_proc
                )

            case self.ui.tab_document:
                cipher.set_reset_state_flag(False)

                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                # We get the path to the output file from the user.
                file_path_output, _ = QFileDialog.getSaveFileName(
                    parent=self,
                    caption="Save new file",
                    directory="",
                    filter=XOR_SUPPORT_EXT,
                )

                if not file_path_output:
                    return

                thread_worker = DataProcessing(
                    cipher=cipher,
                    input_file_path=self.file_path.toLocalFile(),
                    output_file_path=file_path_output,
                    mode="file",
                    enc_proc=enc_proc,
                )

            case _:
                assert False

        self.thread_ready.emit(thread_worker)

    def _tab_document_processing(self, cipher: XOR, enc_proc: EncProc) -> None:
        """Method for encryption on the document processing tab."""
        if self.file_path.isEmpty():
            QMessageBox.warning(self, "Warning!", "File not selected!")
            return

        # We get the path to the output file from the user.
        file_path_output, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save new file",
            directory="",
            filter=XOR_SUPPORT_EXT,
        )

        if not file_path_output:
            return


    def _action_gen_iv_clicked(self) -> None:
        """Method for generating an initialization vector."""
        iv = np.random.randint(0, 256, self.ui.spin_box_iv_size.value())
        iv_hex = bytes(tuple(iv)).hex()
        self.ui.line_edit_iv.setText(iv_hex)

    def _action_save_iv_clicked(self) -> None:
        """Method for storing initialization vector."""
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

    def _action_load_iv_clicked(self) -> None:
        """Method for loading initialization vector."""
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
        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        return bytes(next(rc4) for _ in range(self.ui.spin_box_gamma_size.value())).hex()

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file



class DataProcessing(BaseQThread):
    def __init__(
            self,
            cipher: XOR,
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

            while (block := input_buffer.read(self._read_block_size)) and self._is_worked:
                processed_block = self._cipher.make(block, self._enc_proc)
                output_buffer.write(processed_block)

                self.pbar.emit((PBar.Commands.SET_VALUE, input_buffer.tell()))

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

