# This module contains the implementation of the widget for working
# with the encryption algorithm "RSA".
import json
from typing import Optional, Literal
from io import BytesIO

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
    QLineEdit,
)
from PyQt6.QtCore import QUrl

from .elgamal_ui import Ui_ElgamalDS
from app.crypto.asymmetric import Elgamal
from app.crypto.signatures import ElgamalDS
from app.crypto.hash import (
    SHA1,
    MD5,
    GOST341112,
)
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget,
    BaseQThread,
    PBar,
)
from app.gui.const import ALL_SUPPORT_EXT


HASH_FNS = {
    "SHA1": (SHA1, {}),
    "MD5": (MD5, {}),
    "GOST341112 (256 bit)": (GOST341112, {"iv_size": 256}),
    "GOST341112 (512 bit)": (GOST341112, {"iv_size": 512}),
}


class ElgamalDSWidget(BaseQWidget):
    def __init__(self):
        """RSAWidget class constructor"""
        super(ElgamalDSWidget, self).__init__()
        self.ui = Ui_ElgamalDS()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Elgamal"

        # Initialization of possible encryption processes.
        self.ui.combo_box_sign_proc.addItems(["Sign", "Verify"])
        self.ui.combo_box_hash_alg.addItems((key for key in HASH_FNS))

        # Path received from dragdrop widget
        self.file_path = QUrl()

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(ALL_SUPPORT_EXT)
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
                x = self.ui.line_edit_pr_x.text()
                g = self.ui.line_edit_pr_g.text()
                p = self.ui.line_edit_pr_p.text()

                if not (x and p and g):
                    QMessageBox.warning(self, "Warning!", "Private key values must not be empty!")
                    return

                try:
                    pr_key = ElgamalDS.PrivateKey(int(x, 16), int(g, 16), int(p, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Private key values must be in hexadecimal!")
                    return

                sign_elgamal = ElgamalDS(pr_key=pr_key)

            case "verify":
                y = self.ui.line_edit_pb_y.text()
                g = self.ui.line_edit_pb_g.text()
                p = self.ui.line_edit_pb_p.text()

                if not (y and g and p):
                    QMessageBox.warning(self, "Warning!", "Public key values must not be empty!")
                    return

                try:
                    pb_key = ElgamalDS.PublicKey(int(y, 16), int(g, 16), int(p, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Public key values must be in hexadecimal!")
                    return

                sign_elgamal = ElgamalDS(pb_key=pb_key)

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
                    sign_fn=sign_elgamal,
                    line_edit_r=self.ui.line_edit_sign_r,
                    line_edit_s=self.ui.line_edit_sign_s,
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
                    sign_fn=sign_elgamal,
                    line_edit_r=self.ui.line_edit_sign_r,
                    line_edit_s=self.ui.line_edit_sign_s,
                    sign_proc=sign_proc,
                    input_file_path=self.file_path.toLocalFile(),
                    mode="file",
                )

            case _:
                assert False

        self.thread_ready.emit(thread_worker)

    def _action_gen_keys_clicked(self) -> None:
        """Method for generating keys."""
        key_size = self.ui.spin_box_key_size.value()
        pr_key, pb_key = Elgamal.gen_keys(key_size)

        self.ui.line_edit_pr_p.setText(hex(pr_key.p)[2:])
        self.ui.line_edit_pr_x.setText(hex(pr_key.x)[2:])
        self.ui.line_edit_pr_g.setText(hex(pr_key.g)[2:])

        self.ui.line_edit_pb_g.setText(hex(pb_key.g)[2:])
        self.ui.line_edit_pb_p.setText(hex(pb_key.p)[2:])
        self.ui.line_edit_pb_y.setText(hex(pb_key.y)[2:])

    def _action_save_signature_clicked(self):
        data = {
            "sign": {
                "r": self.ui.line_edit_sign_r.text(),
                "s": self.ui.line_edit_sign_s.text(),
            },
            "y": self.ui.line_edit_pb_y.text(),
            "g": self.ui.line_edit_pb_g.text(),
            "p": self.ui.line_edit_pb_p.text(),
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
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

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

        self.ui.line_edit_sign_r.setText(data.get("sign", {}).get("r", ""))
        self.ui.line_edit_sign_s.setText(data.get("sign", {}).get("s", ""))

        self.ui.line_edit_pb_g.setText(data.get("g", ""))
        self.ui.line_edit_pb_p.setText(data.get("p", ""))
        self.ui.line_edit_pb_y.setText(data.get("y", ""))

    def _action_save_pr_key_clicked(self):
        data = {
            "x": self.ui.line_edit_pr_x.text(),
            "g": self.ui.line_edit_pr_g.text(),
            "p": self.ui.line_edit_pr_p.text(),
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
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

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

        self.ui.line_edit_pr_p.setText(data.get("p", ""))
        self.ui.line_edit_pr_x.setText(data.get("x", ""))
        self.ui.line_edit_pr_g.setText(data.get("g", ""))

    def _action_save_pb_key_clicked(self):
        """Method for storing keys."""
        data = {
            "g": self.ui.line_edit_pb_g.text(),
            "p": self.ui.line_edit_pb_p.text(),
            "y": self.ui.line_edit_pb_y.text(),
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
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

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

        self.ui.line_edit_pb_g.setText(data.get("g", ""))
        self.ui.line_edit_pb_p.setText(data.get("p", ""))
        self.ui.line_edit_pb_y.setText(data.get("y", ""))

    def _save_data_in_file(self, data: dict):
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
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

    def _load_data_from_file(self) -> dict | None:
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
                return json.loads(ifile.read())

        except json.JSONDecodeError:
            QMessageBox.warning(self, "Warning!", "Error reading data, check the correctness of the data!")
            return

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to open file!")
            return

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file


class DataProcessing(BaseQThread):
    def __init__(
            self,
            hash_fn: MD5,
            sign_fn: ElgamalDS,
            line_edit_r: QLineEdit,
            line_edit_s: QLineEdit,
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
        self._line_edit_r = line_edit_r
        self._line_edit_s = line_edit_s
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
                self._line_edit_r.setText(hex(sign.r)[2:])
                self._line_edit_s.setText(hex(sign.s)[2:])

            case "verify":
                sign = ElgamalDS.Signature(
                    int(self._line_edit_r.text(), 16),
                    int(self._line_edit_s.text(), 16),
                )

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
