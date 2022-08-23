# This module contains the implementation of the widget for working
# with the encryption algorithm "GOST 28147-89".
from random import randbytes
import json

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
)
from PyQt6.QtCore import QUrl

from .gost_ui import Ui_GOST
from app.crypto.symmetric import GOST
from app.crypto.exceptions import GOSTError
from app.crypto.common import EncProc
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget
)
from app.gui.const import (
    DES_SUPPORT_EXT,
    MAX_BYTES_READ
)
from app.gui.file_processing import FileProcessing


class GOSTWidget(BaseQWidget):
    def __init__(self):
        """GOSTWidget class constructor"""
        super(GOSTWidget, self).__init__()
        self.ui = Ui_GOST()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "GOST 28147-89"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))
        self.ui.combo_box_enc_mode.addItems((item.name for item in GOST.EncMode))

        # Path received from dragdrop widget
        self.file_path = QUrl()

        # Create a dragdrop widget and place it on the document tab.
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

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _action_gen_iv_clicked(self):
        """Method for generating an initialization vector."""
        self.ui.line_edit_iv.setText(randbytes(8).hex())

    def _action_gen_key_clicked(self):
        """Method for generating a key."""
        self.ui.line_edit_key.setText(randbytes(32).hex())

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
        enc_mode = GOST.EncMode.from_str(self.ui.combo_box_enc_mode.currentText())
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        try:
            cipher = GOST(key_hex, iv_hex, enc_mode)

        except GOSTError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case self.ui.tab_document:
                cipher.set_reset_iv_flag(False)
                self._tab_document_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: GOST, enc_proc: EncProc):
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_data = cipher.make(data, enc_proc)

        except GOSTError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_data)

    def _tab_document_processing(self, cipher: GOST, enc_proc: EncProc):
        """Method for encryption on the document processing tab."""
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

        # We create a stream object that will encrypt the contents of the file, then we send
        # the object to the main window, which will launch it.
        thread_worker = FileProcessing(
            cipher=cipher, enc_proc=enc_proc, input_file=self.file_path.toLocalFile(), output_file=file_path_output,
            input_file_mode="rb", output_file_mode="wb", file_size_control=True, read_block_size=MAX_BYTES_READ,
            control_block_size=8
        )
        self.thread_ready.emit(thread_worker)

    def _file_path_changed(self, file: QUrl):
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file
