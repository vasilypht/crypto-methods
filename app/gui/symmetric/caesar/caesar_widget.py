from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QHBoxLayout,
    QFileDialog
)
from PyQt6.QtCore import (
    QUrl
)

from .caesar_ui import Ui_caesar
from app.crypto.symmetric import caesar
from app.gui.widgets import DragDropWidget
from app.gui.const import (
    MAX_CHARS_READ,
    CAESAR_SUPPORT_EXT
)


class CaesarWidget(QWidget):
    def __init__(self):
        super(CaesarWidget, self).__init__()
        self.ui = Ui_caesar()
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

        self.ui.button_make.clicked.connect(self.button_make_clicked)

    def button_make_clicked(self) -> None:
        """Caesar | (Slot) Method for handling button click. (Encryption/decryption)"""

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_document:
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

                # Attempt to open input file
                try:
                    file_input = open(self.file_path_input.toLocalFile(), "r")
                except OSError:
                    QMessageBox.warning(self, "Warning!", "Error opening input file!")
                    return

                # Attempt to open output file
                try:
                    file_output = open(file_path_output, "w")
                except OSError:
                    # Closing the input file
                    file_input.close()
                    QMessageBox.warning(self, "Warning!", "Error opening output file!")
                    return

                try:
                    while block := file_input.read(MAX_CHARS_READ):
                        processed_block = caesar.make(
                            text=block,
                            shift=self.ui.spin_box_shift.value(),
                            mode=self.ui.combo_box_mode.currentText().lower()
                        )
                        file_output.write(processed_block)
                except caesar.CaesarError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

                finally:
                    file_input.close()
                    file_output.close()

            case self.ui.tab_text:
                try:
                    processed_text = caesar.make(
                        text=self.ui.text_edit_input.toPlainText(),
                        shift=self.ui.spin_box_shift.value(),
                        mode=self.ui.combo_box_mode.currentText().lower()
                    )
                except caesar.CaesarError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

                self.ui.text_edit_output.setText(processed_text)

    def _change_file_path(self, file: QUrl):
        self.file_path_input = file
