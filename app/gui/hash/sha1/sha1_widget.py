# This module contains the implementation of the widget for working
# with the encryption algorithm "RSA".
from typing import Literal, Optional
from io import BytesIO

from PyQt6.QtWidgets import (
    QMessageBox,
    QLineEdit,
    QVBoxLayout
)
from PyQt6.QtCore import QUrl

from app.gui.hash.sha1.sha1_ui import Ui_SHA1
from app.crypto.hash import SHA1
from app.gui.widgets import (
    DragDropWidget,
    BaseQThread,
    BaseQWidget,
    PBar
)
from app.gui.const import ALL_SUPPORT_EXT


class SHA1Widget(BaseQWidget):
    def __init__(self) -> None:
        """RSAWidget class constructor"""
        super(SHA1Widget, self).__init__()
        self.ui = Ui_SHA1()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "SHA1"

        # Path received from dragdrop widget
        self.file_path = QUrl()

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(ALL_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                thread_worker = DataProcessing(
                    hash_fn=SHA1(),
                    input_string=self.ui.text_edit_input.toPlainText(),
                    output_line_edit=self.ui.line_edit_result,
                    mode="string",
                )

            case self.ui.tab_document:
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                thread_worker = DataProcessing(
                    hash_fn=SHA1(),
                    input_file_path=self.file_path.toLocalFile(),
                    output_line_edit=self.ui.line_edit_result,
                    mode="file",
                )

            case _:
                assert False

        self.thread_ready.emit(thread_worker)

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file


class DataProcessing(BaseQThread):
    def __init__(
            self,
            hash_fn: SHA1,
            output_line_edit: QLineEdit,
            *,
            input_string: str = "",
            input_file_path: Optional[str] = None,
            mode: Literal["file", "string"] = "string",
            **options
    ) -> None:
        super(DataProcessing, self).__init__()

        self._hash_fn = hash_fn
        self._out_line_edit = output_line_edit
        self._input_string = input_string
        self._input_file_path = input_file_path
        self._mode = mode

        self._read_block_size = options.get("read_block_size", 4096)

        self._is_worked = True

    def close(self) -> None:
        self._is_worked = False
        self.wait()

    def run(self) -> None:
        match self._mode:
            case "file":
                try:
                    buffer = open(self._input_file_path, "rb")
                except IOError:
                    self.message.emit((
                        BaseQThread.MessageType.WARNING,
                        "Warning!",
                        "Error opening file!",
                    ))
                    return

            case "string":
                buffer = BytesIO(self._input_string.encode("utf-8"))

            case _:
                assert False

        try:
            buffer.seek(0, 2)
            buffer_size = buffer.tell()
            buffer.seek(0, 0)

            if buffer_size == 0:
                self._out_line_edit.setText(self._hash_fn.hexdigest)
                return

            self.pbar.emit((PBar.Commands.SET_RANGE, 0, buffer_size))
            self.pbar.emit((PBar.Commands.SET_VALUE, 0))
            self.pbar.emit((PBar.Commands.SHOW,))

            self._hash_fn._drop_buffer()

            # We read a piece of data, encrypt it and write it to the output file,
            # simultaneously updating the value in the progress bar.
            while (block := buffer.read(self._read_block_size)) and self._is_worked:
                self._hash_fn._block_processing(
                    block=block,
                    read_block_size=self._read_block_size,
                    buffer_size=buffer_size,
                )

                self.pbar.emit((PBar.Commands.SET_VALUE, buffer.tell()))

            if self._is_worked:
                self._out_line_edit.setText(self._hash_fn._collect().hex())

        except Exception as e:
            self.message.emit((
                BaseQThread.MessageType.CRITICAL,
                "Unknown error!",
                "An error occurred while working with file or when determining the file size.\n"
                f"({e.args[0]})"
            ))

        finally:
            buffer.close()
            self.pbar.emit((PBar.Commands.CLOSE,))
