# This module contains the implementation of the widget for working
# with the encryption algorithm "RSA".
import json
from io import BytesIO
from typing import Literal, Optional

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
    QLineEdit,
)
from PyQt6.QtCore import QUrl

from .rsa_ui import Ui_RSADS
from app.crypto.asymmetric import RSA
from app.crypto.signatures import RSADS
from app.crypto.hash import (SHA1, MD5, GOST341112)
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget,
    BaseQThread,
    PBar,
)
from app.gui.const import RSA_SUPPORT_EXT


HASH_FNS = {
    "SHA1": (SHA1, {}),
    "MD5": (MD5, {}),
    "GOST341112 (256 bit)": (GOST341112, {"iv_size": 256}),
    "GOST341112 (512 bit)": (GOST341112, {"iv_size": 512}),
}


class RSADSWidget(BaseQWidget):
    def __init__(self):
        """RSAWidget class constructor"""
        super(RSADSWidget, self).__init__()
        self.ui = Ui_RSADS()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "RSA"

        # Initialization of possible encryption processes.
        self.ui.combo_box_sign_proc.addItems(["Sign", "Verify"])
        self.ui.combo_box_hash_alg.addItems((key for key in HASH_FNS))

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
                n = self.ui.line_edit_pr_module.text()
                d = self.ui.line_edit_pr_key.text()

                if not (n and d):
                    QMessageBox.warning(self, "Warning!", "Private key values must not be empty!")
                    return

                try:
                    pr_key = RSADS.PrivateKey(int(d, 16), int(n, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Private key values must be in hexadecimal!")
                    return

                sign_rsa = RSADS(pr_key=pr_key)

            case "verify":
                n = self.ui.line_edit_pb_module.text()
                e = self.ui.line_edit_pb_key.text()

                if not (n and e):
                    QMessageBox.warning(self, "Warning!", "Public key values must not be empty!")
                    return

                try:
                    pb_key = RSADS.PublicKey(int(e, 16), int(n, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Public key values must be in hexadecimal!")
                    return

                sign_rsa = RSADS(pb_key=pb_key)

            case _:
                assert False

        hash_fn_type, kwargs = HASH_FNS.get(self.ui.combo_box_hash_alg.currentText(), (None, None))
        if not hash_fn_type:
            QMessageBox.warning(self, "Warning!", "Hash function not found!")
            return

        hash_fn = hash_fn_type(**kwargs)

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                thread_worker = DataProcessing(
                    hash_fn=hash_fn,
                    sign_fn=sign_rsa,
                    sign_proc=sign_proc,
                    line_edit_sign=self.ui.line_edit_sign,
                    input_string=self.ui.text_edit_input.toPlainText(),
                    mode="string",
                )

            case self.ui.tab_document:
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                thread_worker = DataProcessing(
                    hash_fn=hash_fn,
                    sign_fn=sign_rsa,
                    sign_proc=sign_proc,
                    line_edit_sign=self.ui.line_edit_sign,
                    input_file_path=self.file_path.toLocalFile(),
                    mode="file",
                )

            case _:
                assert False

        self.thread_ready.emit(thread_worker)

    def _action_gen_keys_clicked(self) -> None:
        """Method for generating keys."""
        key_size = self.ui.spin_box_key_size.value()
        pr_key, pb_key = RSA.gen_keys(key_size)

        self.ui.line_edit_pr_key.setText(hex(pr_key.d)[2:])
        self.ui.line_edit_pr_module.setText(hex(pr_key.n)[2:])
        self.ui.line_edit_pb_key.setText(hex(pb_key.e)[2:])
        self.ui.line_edit_pb_module.setText(hex(pb_key.n)[2:])

    def _action_save_signature_clicked(self):
        data = {
            "sign": self.ui.line_edit_sign.text(),
            "e": self.ui.line_edit_pb_key.text(),
            "n": self.ui.line_edit_pb_module.text(),
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
        self.ui.line_edit_pb_key.setText(data.get("e", ""))
        self.ui.line_edit_pb_module.setText(data.get("n", ""))

    def _action_save_pr_key_clicked(self):
        data = {
            "d": self.ui.line_edit_pr_key.text(),
            "n": self.ui.line_edit_pr_module.text(),
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

        self.ui.line_edit_pr_key.setText(data.get("d", ""))
        self.ui.line_edit_pr_module.setText(data.get("n", ""))

    def _action_save_pb_key_clicked(self):
        data = {
            "e": self.ui.line_edit_pb_key.text(),
            "n": self.ui.line_edit_pb_module.text(),
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

        self.ui.line_edit_pb_key.setText(data.get("e", ""))
        self.ui.line_edit_pb_module.setText(data.get("n", ""))

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file


class DataProcessing(BaseQThread):
    def __init__(
            self,
            hash_fn: MD5,
            sign_fn: RSADS,
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
