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
from app.crypto.exceptions import CaesarError
from app.crypto.common import EncProc
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
        thread_worker = FileProcessing(cipher, enc_proc, self.input_file_path.toLocalFile(), file_path_output)
        self.thread_ready.emit(thread_worker)

    def _change_file_path(self, file: QUrl):
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.input_file_path = file


class FileProcessing(BaseQThread):
    def __init__(self, cipher: Caesar, enc_proc: EncProc, input_file: str, output_file: str) -> None:
        """
        FileProcessing class constructor. This class is designed to encrypt
        a file in a separate stream.

        Args:
            cipher: The cipher with which the file will be encrypted. This cipher
                must have an interface "make".

            enc_proc: parameter responsible for the process of data encryption
                (encryption and decryption).

            input_file: the path to the input file to be encrypted.
            output_file: path to the output file to be written to.
        """
        super(FileProcessing, self).__init__()
        self._cipher = cipher
        self._enc_proc = enc_proc
        self._input_file = input_file
        self._output_file = output_file

        self._is_worked = True

    def close(self):
        """Method for stopping a thread"""
        # The flag is set to false and then we start to wait
        # until the loop in the thread stops.
        self._is_worked = False
        self.wait()

    def run(self) -> None:
        """The method that is called after the thread has started via the "start" method"""
        try:
            with open(self._input_file, "r") as input_file, \
                    open(self._output_file, "w") as output_file:
                # Find out the file size (number of bytes - if binary format,
                # number of characters - if normal)
                input_file.seek(0, 2)
                input_file_size = input_file.tell()
                input_file.seek(0, 0)

                # Initializes the progress bar by sending signals to the main window.
                self.pbar.emit((PBarCommands.SET_RANGE, 0, input_file_size))
                self.pbar.emit((PBarCommands.SET_VALUE, 0))
                self.pbar.emit((PBarCommands.SHOW,))

                # We read a piece of data, encrypt it and write it to the output file,
                # simultaneously updating the value in the progress bar.
                while (block := input_file.read(MAX_CHARS_READ)) and self._is_worked:
                    encrypted_block = self._cipher.make(block, self._enc_proc)
                    output_file.write(encrypted_block)

                    self.pbar.emit((PBarCommands.SET_VALUE, input_file.tell()))

        except Exception as e:
            # If an exception occurs, we send an error message.
            self.message.emit("An error occurred while working with files or when "
                              "determining the file size. (Check encryption mode)\n"
                              f"({e.args[0]})")

        finally:
            # Close the processbar.
            self.pbar.emit((PBarCommands.CLOSE,))

