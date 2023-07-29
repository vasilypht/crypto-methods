# This module contains the implementation of the widget for working
# with the encryption algorithm "RSA".
from typing import Literal, Optional
import json
from io import BytesIO

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
    QLineEdit,
)
from PyQt6.QtCore import QUrl

from .gost341112_ui import Ui_GOST341112DS
from app.crypto.signatures import GOST341112DS
from app.crypto.hash import GOST341112
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget,
    BaseQThread,
    PBar
)
from app.gui.const import RSA_SUPPORT_EXT


AVAILABLE_CURVES = (
    "gost256",
    "gost512",
)


class GOST341112DSWidget(BaseQWidget):
    def __init__(self):
        """RSAWidget class constructor"""
        super(GOST341112DSWidget, self).__init__()
        self.ui = Ui_GOST341112DS()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "GOST 34.11-2012"

        # Initialization of possible encryption processes.
        self.ui.combo_box_sign_proc.addItems(["Sign", "Verify"])
        self.ui.combo_box_curve.addItems((name for name in AVAILABLE_CURVES))

        # Path received from dragdrop widget
        self.file_path = QUrl()

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(RSA_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Context menu
        menu = QMenu()
        menu.addAction("Generate keys", self._action_gen_keys_clicked)
        menu.addSeparator()
        menu.addAction("Save signature", self._action_save_signature_clicked)
        menu.addAction("Load signature", self._action_load_signature_clicked)
        menu.addSeparator()
        menu.addAction("Save private key", self._action_save_pr_key_clicked)
        menu.addAction("Load private key", self._action_load_pr_key_clicked)
        menu.addSeparator()
        menu.addAction("Save Public key", self._action_save_pb_key_clicked)
        menu.addAction("Load Public key", self._action_load_pb_key_clicked)

        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        sign_proc = self.ui.combo_box_sign_proc.currentText().lower()

        match sign_proc:
            case "sign":
                d = self.ui.line_edit_pr_key_d.text()

                if not d:
                    QMessageBox.warning(self, "Warning!", "Private key values must not be empty!")
                    return

                try:
                    pr_key = GOST341112DS.PrivateKey(int(d, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Private key values must be in hexadecimal!")
                    return

                sign_gost = GOST341112DS(pr_key=pr_key, curve=self.ui.combo_box_curve.currentText())

            case "verify":
                x = self.ui.line_edit_pb_key_x.text()
                y = self.ui.line_edit_pb_key_y.text()

                if not (x and y):
                    QMessageBox.warning(self, "Warning!", "Public key values must not be empty!")
                    return

                try:
                    pb_key = GOST341112DS.PublicKey(int(x, 16), int(y, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Public key values must be in hexadecimal!")
                    return

                sign_gost = GOST341112DS(pb_key=pb_key, curve=self.ui.combo_box_curve.currentText())

            case _:
                assert False

        hash_fn = GOST341112(iv_size=sign_gost.hash_dimension)

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                thread_worker = DataProcessing(
                    hash_fn=hash_fn,
                    sign_fn=sign_gost,
                    line_edit_sign=self.ui.line_edit_sign,
                    sign_proc=sign_proc,
                    input_string=self.ui.text_edit_input.toPlainText(),
                    mode="string",
                )

            case self.ui.tab_document:
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                thread_worker = DataProcessing(
                    hash_fn=hash_fn,
                    sign_fn=sign_gost,
                    line_edit_sign=self.ui.line_edit_sign,
                    sign_proc=sign_proc,
                    input_file_path=self.file_path.toLocalFile(),
                    mode="file",
                )

            case _:
                assert False

        self.thread_ready.emit(thread_worker)

    def _action_gen_keys_clicked(self) -> None:
        """Method for generating keys."""
        pr_key, pb_key = GOST341112DS.gen_keys(self.ui.combo_box_curve.currentText())

        self.ui.line_edit_pr_key_d.setText(hex(pr_key.d)[2:])

        self.ui.line_edit_pb_key_x.setText(hex(pb_key.x)[2:])
        self.ui.line_edit_pb_key_y.setText(hex(pb_key.y)[2:])

    def _action_save_signature_clicked(self):
        data = {
            "curve": self.ui.combo_box_curve.currentText(),
            "sign": self.ui.line_edit_sign.text(),
            "point": {
                "x": self.ui.line_edit_pb_key_x.text(),
                "y": self.ui.line_edit_pb_key_y.text(),
            },
        }

        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save a key file",
            directory="",
            filter="All files (*)",
            initialFilter="All files (*)"
        )

        if not filename:
            return

        try:
            with open(filename, "w") as ofile:
                ofile.write(json.dumps(data))

        except OSError:
            raise QMessageBox.warning(self, "Warning!", "Failed to save file!")

    def _action_load_signature_clicked(self):
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
            with open(filename, "r") as ifile:
                data = json.loads(ifile.read())

        except json.JSONDecodeError:
            QMessageBox.warning(self, "Warning!", "Error reading data, check the correctness of the data!")
            return

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

        self.ui.line_edit_sign.setText(data.get("sign", ""))
        self.ui.line_edit_pb_key_x.setText(data.get("point", "").get("x"))
        self.ui.line_edit_pb_key_y.setText(data.get("point", "").get("y"))
        self.ui.combo_box_curve.setCurrentText(data.get("curve", AVAILABLE_CURVES[0]))

    def _action_save_pr_key_clicked(self):
        data = {
            "d": self.ui.line_edit_pr_key_d.text(),
        }

        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save a key file",
            directory="",
            filter="All files (*)",
            initialFilter="All files (*)"
        )

        if not filename:
            return

        try:
            with open(filename, "w") as ofile:
                ofile.write(json.dumps(data))

        except OSError:
            raise QMessageBox.warning(self, "Warning!", "Failed to save file!")

    def _action_load_pr_key_clicked(self):
        """Method for loading the keys."""
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
            with open(filename, "r") as ifile:
                data = json.loads(ifile.read())

        except json.JSONDecodeError:
            QMessageBox.warning(self, "Warning!", "Error reading data, check the correctness of the data!")
            return

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

        self.ui.line_edit_pr_key_d.setText(data.get("d", ""))

    def _action_save_pb_key_clicked(self):
        data = {
            "point": {
                "x": self.ui.line_edit_pb_key_x.text(),
                "y": self.ui.line_edit_pb_key_y.text(),
            }
        }

        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save a key file",
            directory="",
            filter="All files (*)",
            initialFilter="All files (*)"
        )

        if not filename:
            return

        try:
            with open(filename, "w") as ofile:
                ofile.write(json.dumps(data))

        except OSError:
            raise QMessageBox.warning(self, "Warning!", "Failed to save file!")

    def _action_load_pb_key_clicked(self):
        """Method for loading the keys."""
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
            with open(filename, "r") as ifile:
                data = json.loads(ifile.read())

        except json.JSONDecodeError:
            QMessageBox.warning(self, "Warning!", "Error reading data, check the correctness of the data!")
            return

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

        self.ui.line_edit_pb_key_x.setText(data.get("point", "").get("x", ""))
        self.ui.line_edit_pb_key_x.setText(data.get("point", "").get("y", ""))

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file


class DataProcessing(BaseQThread):
    def __init__(
            self,
            hash_fn: GOST341112,
            sign_fn: GOST341112DS,
            line_edit_sign: QLineEdit,
            *,
            input_string: str = "",
            input_file_path: Optional[str] = None,
            sign_proc: Literal["sign", "verify"] = "sign",
            mode: Literal["file", "string"] = "string",
            **options
    ) -> None:
        super(DataProcessing, self).__init__()

        self._hash_fn = hash_fn
        self._sign_fn = sign_fn
        self._line_edit_sign = line_edit_sign
        self._input_string = input_string
        self._input_file_path = input_file_path
        self._sign_proc = sign_proc
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

        hash_hvalue = ""

        try:
            buffer.seek(0, 2)
            buffer_size = buffer.tell()
            buffer.seek(0, 0)

            if buffer_size == 0:
                hash_hvalue = self._hash_fn.hexdigest
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
                hash_hvalue = self._hash_fn._collect().hex()
            else:
                return

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

        match self._sign_proc:
            case "sign":
                sign = self._sign_fn.sign(hash_hvalue)
                self._line_edit_sign.setText(sign)

            case "verify":
                sign = self._line_edit_sign.text()

                if self._sign_fn.verify(sign, hash_hvalue):
                    self.message.emit((
                        BaseQThread.MessageType.INFORMATION,
                        "ElGamal digital signature",
                        "The signatures match, the file is original!"
                    ))
                else:
                    self.message.emit((
                        BaseQThread.MessageType.INFORMATION,
                        "ElGamal digital signature",
                        "Signatures do not match, the file is not original!"
                    ))

            case _:
                assert False

