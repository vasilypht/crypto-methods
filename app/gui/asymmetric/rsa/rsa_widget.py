# This module contains the implementation of the widget for working
# with the encryption algorithm "RSA".
from io import BytesIO
from typing import Literal, Optional
import json

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout,
    QTextEdit,
)
from PyQt6.QtCore import QUrl

from sympy import isprime

from .rsa_ui import Ui_RSA
from app.crypto.asymmetric import RSA
from app.crypto.common import EncProc
from app.crypto.utils import gen_prime
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget,
    BaseQThread,
    PBar,
)
from app.gui.const import ALL_SUPPORT_EXT


class RSAWidget(BaseQWidget):
    def __init__(self):
        """RSAWidget class constructor"""
        super(RSAWidget, self).__init__()
        self.ui = Ui_RSA()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "RSA"

        # Initialization of possible encryption processes.
        self.ui.combo_box_enc_proc.addItems((item.name.capitalize() for item in EncProc))

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
        menu.addAction("Generate keys from p and q", self._action_gen_keys_from_p_q_clicked)
        menu.addAction("Generate p and q", self._action_gen_p_q_clicked)
        menu.addSeparator()
        menu.addAction("Save private key", self._action_save_pr_key_clicked)
        menu.addAction("Load private key", self._action_load_pr_key_clicked)
        menu.addSeparator()
        menu.addAction("Save public key", self._action_save_pb_key_clicked)
        menu.addAction("Load public key", self._action_load_pb_key_clicked)

        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        # read private key
        match enc_proc:
            case EncProc.ENCRYPT:
                n = self.ui.line_edit_pb_module.text()
                e = self.ui.line_edit_pb_key.text()

                if not (n and e):
                    QMessageBox.warning(self, "Warning!", "Public key values must not be empty!")
                    return

                try:
                    pb_key = RSA.PublicKey(int(e, 16), int(n, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Public key values must be in hexadecimal!")
                    return

                cipher = RSA(public_key=pb_key)

            case EncProc.DECRYPT:
                n = self.ui.line_edit_pr_module.text()
                d = self.ui.line_edit_pr_key.text()

                if not (n and d):
                    QMessageBox.warning(self, "Warning!", "Private key values must not be empty!")
                    return

                try:
                    pr_key = RSA.PrivateKey(int(d, 16), int(n, 16))
                except ValueError:
                    QMessageBox.warning(self, "Warning!", "Private key values must be in hexadecimal!")
                    return

                cipher = RSA(private_key=pr_key)
            case _:
                assert False

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self.ui.text_edit_output.setText("")

                thread_worker = DataProcessing(
                    cipher=cipher,
                    enc_proc=enc_proc,
                    output_text_edit=self.ui.text_edit_output,
                    input_string=self.ui.text_edit_input.toPlainText(),
                    mode="string",
                )

            case self.ui.tab_document:
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                # We get the path to the output file from the user.
                file_path_output, _ = QFileDialog.getSaveFileName(
                    parent=self,
                    caption="Save new file",
                    directory="",
                    filter=ALL_SUPPORT_EXT,
                )

                if not file_path_output:
                    return

                thread_worker = DataProcessing(
                    cipher=cipher,
                    enc_proc=enc_proc,
                    input_file_path=self.file_path.toLocalFile(),
                    output_file_path=file_path_output,
                    mode="file",
                )
            case _:
                assert False

        self.thread_ready.emit(thread_worker)

    def _action_gen_keys_clicked(self) -> None:
        """Method for generating keys."""
        key_size = self.ui.spin_box_key_size.value()
        pr_key, pb_key = RSA.gen_keys(key_size)

        # set private key
        self.ui.line_edit_pr_key.setText(hex(pr_key.d)[2:])
        self.ui.line_edit_pr_module.setText(hex(pr_key.n)[2:])

        # set public key
        self.ui.line_edit_pb_key.setText(hex(pb_key.e)[2:])
        self.ui.line_edit_pb_module.setText(hex(pb_key.n)[2:])

    def _action_gen_keys_from_p_q_clicked(self) -> None:
        """Method for generating keys according to the entered/generated P and Q."""
        p = self.ui.line_edit_p.text()
        q = self.ui.line_edit_q.text()

        if not (p and q):
            QMessageBox.warning(self, "Warning!", "It is necessary to generate P and Q!")
            return

        try:
            p = int(p, 16)
            q = int(q, 16)
        except ValueError:
            QMessageBox.warning(self, "Warning!", "P and Q must be in hexadecimal.")
            return

        if not (isprime(p) and isprime(q)):
            QMessageBox.warning(self, "Warning!", "P and Q must be prime numbers!")
            return

        pr_key, pb_key = RSA.gen_keys(p=p, q=q)

        # set private key
        self.ui.line_edit_pr_key.setText(hex(pr_key.d)[2:])
        self.ui.line_edit_pr_module.setText(hex(pr_key.n)[2:])

        # set public key
        self.ui.line_edit_pb_key.setText(hex(pb_key.e)[2:])
        self.ui.line_edit_pb_module.setText(hex(pb_key.n)[2:])

    def _action_gen_p_q_clicked(self):
        """Method for generating prime numbers P and Q, of given dimension"""
        key_size = self.ui.spin_box_key_size.value()
        p = gen_prime(key_size)
        q = gen_prime(key_size)

        self.ui.line_edit_p.setText(hex(p)[2:])
        self.ui.line_edit_q.setText(hex(q)[2:])

    def _action_save_pr_key_clicked(self):
        """Method for storing keys."""
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

    def _action_save_pb_key_clicked(self):
        """Method for storing keys."""
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

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file


class DataProcessing(BaseQThread):
    def __init__(
            self,
            cipher: RSA,
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

            match self._enc_proc:
                case EncProc.ENCRYPT:
                    read_block_size = self._cipher.num_bytes_public_module - 1

                    enc_size = self._cipher.encrypt(input_buffer_size)
                    enc_size_block = enc_size.to_bytes(self._cipher.num_bytes_public_module, "little")
                    output_buffer.write(enc_size_block)

                case EncProc.DECRYPT:
                    read_block_size = self._cipher.num_bytes_private_module

                    enc_size_block = input_buffer.read(self._cipher.num_bytes_private_module)
                    enc_size = int.from_bytes(enc_size_block, "little")
                    final_file_size = self._cipher.decrypt(enc_size)

                case _:
                    assert False

            while (block := input_buffer.read(read_block_size)) and self._is_worked:
                processed_block = self._cipher.make(block, self._enc_proc, "little")
                output_buffer.write(processed_block)

                self.pbar.emit((PBar.Commands.SET_VALUE, input_buffer.tell()))

            if self._enc_proc == EncProc.DECRYPT:
                output_buffer.truncate(final_file_size)

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
