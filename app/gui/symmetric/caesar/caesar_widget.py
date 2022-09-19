# This module contains the implementation of the widget for working
# with the encryption algorithm "Caesar's cipher".
from PyQt6.QtWidgets import (
    QMessageBox,
    QHBoxLayout,
    QFileDialog
)
from PyQt6.QtCore import QUrl

from .caesar_ui import Ui_Caesar
from app.crypto.symmetric import Caesar
from app.crypto.common import EncProc
from app.gui.const import (
    MAX_CHARS_READ,
    CAESAR_SUPPORT_EXT
)
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget
)
from app.gui.file_processing import FileProcessing


class CaesarWidget(BaseQWidget):
    def __init__(self):
        """CaesarWidget class constructor"""
        super(CaesarWidget, self).__init__()
        self.ui = Ui_Caesar()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Caesar"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

        # Path received from dragdrop widget
        self.input_file_path = QUrl()

        # Create a dragdrop widget and place it on the document tab.
        self.drag_drop_widget = DragDropWidget()
        self.drag_drop_widget.set_filter_extensions(CAESAR_SUPPORT_EXT)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.drag_drop_widget)
        self.ui.tab_document.setLayout(layout)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._change_file_path)
        self.drag_drop_widget.canceled.connect(self._change_file_path)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        # Getting data from a form
        shift = self.ui.spin_box_shift.value()
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        cipher = Caesar(shift)

        # Depending on which widget is active, select the appropriate action.
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case self.ui.tab_document:
                self._tab_document_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: Caesar, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        # Getting data from a form
        data = self.ui.text_edit_input.toPlainText()

        # We call the "make" method, and pass data and processing type to it.
        try:
            processed_text = cipher.make(data, enc_proc)

        except CaesarError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_text)

    def _tab_document_processing(self, cipher: Caesar, enc_proc: EncProc):
        """Method for encryption on the document processing tab."""
        # If the path of the input file is not set, then we exit the method.
        if self.input_file_path.isEmpty():
            QMessageBox.warning(self, "Warning!", "File not selected!")
            return

        # We get the path to the output file from the user.
        file_path_output, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save new file",
            directory="",
            filter=CAESAR_SUPPORT_EXT,
        )

        # If the path is not set, exit the method.
        if not file_path_output:
            return

        # We create a stream object that will encrypt the contents of the file, then we send
        # the object to the main window, which will launch it.
        thread_worker = FileProcessing(
            cipher=cipher, enc_proc=enc_proc, input_file=self.input_file_path.toLocalFile(),
            output_file=file_path_output, input_file_mode="r", output_file_mode="w", file_size_control=False,
            read_block_size=MAX_CHARS_READ
        )
        self.thread_ready.emit(thread_worker)

    def _change_file_path(self, file: QUrl):
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.input_file_path = file
