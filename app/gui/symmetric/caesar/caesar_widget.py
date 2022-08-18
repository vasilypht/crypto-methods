from PyQt6.QtWidgets import (
    QMessageBox,
    QHBoxLayout,
    QFileDialog
)
from PyQt6.QtCore import QUrl

from .caesar_ui import Ui_Caesar
from app.crypto.symmetric.caesar import (
    Caesar,
    CaesarError
)
from app.gui.const import (
    MAX_CHARS_READ,
    CAESAR_SUPPORT_EXT
)
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget,
    BaseQThread,
    PBarCommands
)


class CaesarWidget(BaseQWidget):
    def __init__(self):
        super(CaesarWidget, self).__init__()
        self.ui = Ui_Caesar()
        self.ui.setupUi(self)

        self.title = "Caesar"

        self.file_path_input = QUrl()

        self.drag_drop_widget = DragDropWidget()
        self.drag_drop_widget.set_filter_extensions(CAESAR_SUPPORT_EXT)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.drag_drop_widget)
        self.ui.tab_document.setLayout(layout)

        self.drag_drop_widget.dropped.connect(self._change_file_path)
        self.drag_drop_widget.canceled.connect(self._change_file_path)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Caesar | (Slot) Method for handling button click. (Encryption/decryption)"""
        shift = self.ui.spin_box_shift.value()
        mode = self.ui.combo_box_mode.currentText().lower()

        cipher = Caesar(shift)

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, mode)

            case self.ui.tab_document:
                self._tab_document_processing(cipher, mode)

            case _:
                pass

    def _tab_text_processing(self, cipher: Caesar, mode: str):
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_text = cipher.make(data, mode)

        except CaesarError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)

    def _tab_document_processing(self, cipher: Caesar, mode: str):
        if self.file_path_input.isEmpty():
            QMessageBox.warning(self, "Warning!", "File not selected!")
            return

        # get the name of the new file
        file_path_output, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save new file",
            directory="",
            filter=CAESAR_SUPPORT_EXT,
        )

        if not file_path_output:
            return

        thread_worker = FileProcessing(cipher, mode, self.file_path_input.toLocalFile(), file_path_output)
        self.thread_ready.emit(thread_worker)

    def _change_file_path(self, file: QUrl):
        self.file_path_input = file


class FileProcessing(BaseQThread):
    def __init__(self, cipher: Caesar, mode: str, input_file: str, output_file: str):
        super(FileProcessing, self).__init__()
        self._cipher = cipher
        self._mode = mode
        self._input_file = input_file
        self._output_file = output_file

        self._is_worked = True

    def close(self):
        self._is_worked = False
        self.wait()

    def run(self) -> None:
        try:
            with open(self._input_file, "r") as input_file, \
                    open(self._output_file, "w") as output_file:
                input_file.seek(0, 2)
                input_file_size = input_file.tell()
                input_file.seek(0, 0)

                self.pbar.emit((PBarCommands.SET_RANGE, 0, input_file_size))
                self.pbar.emit((PBarCommands.SET_VALUE, 0))
                self.pbar.emit((PBarCommands.SHOW,))

                while (block := input_file.read(MAX_CHARS_READ)) and self._is_worked:
                    encrypted_block = self._cipher.make(block, self._mode)
                    output_file.write(encrypted_block)

                    self.pbar.emit((PBarCommands.SET_VALUE, input_file.tell()))

        except Exception as e:
            self.message.emit("An error occurred while working with files or when "
                              "determining the file size. (Check encryption mode)\n"
                              f"({e.args[0]})")

        finally:
            self.pbar.emit((PBarCommands.CLOSE,))

