# This module contains the implementation of the widget for working
# with the encryption algorithm "RSA".
import json

from PyQt6.QtWidgets import (
    QMessageBox,
    QMenu,
    QFileDialog,
    QVBoxLayout
)
from PyQt6.QtCore import QUrl

from sympy import isprime

from .rsa_ui import Ui_RSA
from app.crypto.asymmetric import RSA
from app.crypto.common import EncProc
from app.crypto.utils import gen_prime
from app.gui.file_processing import FileProcessing
from app.gui.widgets import (
    DragDropWidget,
    BaseQWidget
)
from app.gui.const import RSA_SUPPORT_EXT


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
        self.drag_drop_widget.set_filter_extensions(RSA_SUPPORT_EXT)
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
        menu.addAction("Save key", self._action_save_key_clicked)
        menu.addAction("Load key", self._action_load_key_clicked)

        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        enc_proc = EncProc.from_str(self.ui.combo_box_enc_proc.currentText())

        n = self.ui.line_edit_module.text()
        d = self.ui.line_edit_private_key.text()
        e = self.ui.line_edit_public_key.text()

        if not (n and d and e):
            QMessageBox.warning(self, "Warning!", "Key fields must not be empty!")
            return

        try:
            n = int(n, 16)
            d = int(d, 16)
            e = int(e, 16)
        except ValueError:
            QMessageBox.warning(self, "Warning!", "Public, private keys and module must be in hexadecimal.")
            return

        private_key = RSA.PrivateKey(d, n)
        public_key = RSA.PublicKey(e, n)

        try:
            cipher = RSA(private_key, public_key)
        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_processing(cipher, enc_proc)

            case self.ui.tab_document:
                self._tab_document_processing(cipher, enc_proc)

            case _:
                pass

    def _tab_text_processing(self, cipher: ..., enc_proc: EncProc) -> None:
        """Method for encryption on the text processing tab."""
        data = self.ui.text_edit_input.toPlainText()

        try:
            match enc_proc:
                case EncProc.ENCRYPT:
                    # When encrypting, we translate the data into bytes and take the
                    # maximum block size that can be encrypted with the specified module
                    data = data.encode("utf-8")
                    block_size = cipher.num_bytes_to_encrypt

                case EncProc.DECRYPT:
                    # The data is expected to be in hexadecimal format. Convert to
                    # bytes and set the block mode to the number of bytes of the module.
                    data = bytes.fromhex(data)
                    block_size = cipher.num_bytes_to_decrypt

                case _:
                    raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")

            processed_data = []

            for i in range(0, len(data), block_size):
                # Each block of data is processed in accordance with the encryption process.
                block = data[i:i + block_size]
                encrypted_block = cipher.make(block, enc_proc)
                processed_data.append(encrypted_block)

            # The received bytes are combined into one line.
            processed_data = b"".join(processed_data)

            match enc_proc:
                case EncProc.ENCRYPT:
                    # If we encrypt the data, then the bytes are converted
                    # to a hexadecimal format string at the output.
                    processed_data = processed_data.hex()

                case EncProc.DECRYPT:
                    # If we decrypted the data, then the bytes are decoded
                    # into a unicode string at the output.
                    processed_data = processed_data.decode("utf-8")

                case _:
                    raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")

        except Exception as e:
            QMessageBox.warning(self, "Warning!", f"{e.args[0]}")
            return

        self.ui.text_edit_output.setText(processed_data)

    def _tab_document_processing(self, cipher: ..., enc_proc: EncProc) -> None:
        """Method for encryption on the document processing tab."""
        if self.file_path.isEmpty():
            QMessageBox.warning(self, "Warning!", "File not selected!")
            return

        # We get the path to the output file from the user.
        file_path_output, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save new file",
            directory="",
            filter=RSA_SUPPORT_EXT,
        )

        if not file_path_output:
            return

        # Depending on the encryption process, the block size for
        # reading changes. The encryption reads fewer bytes than
        # the modulus length, and then flattens the resulting value
        # to the modulus size. During decryption, as much as the size
        # in bytes of the module is read, then the decrypted data
        # is aligned to the amount that was read during encryption.
        if enc_proc is EncProc.ENCRYPT:
            read_block_size = cipher.num_bytes_to_encrypt
            control_block_size = read_block_size
        else:
            read_block_size = cipher.num_bytes_to_decrypt
            control_block_size = read_block_size

        # We create a stream object that will encrypt the contents of the file, then we send
        # the object to the main window, which will launch it.
        thread_worker = FileProcessing(cipher=cipher, enc_proc=enc_proc, input_file=self.file_path.toLocalFile(),
                                       output_file=file_path_output, input_file_mode="rb", output_file_mode="wb",
                                       file_size_control=True, read_block_size=read_block_size,
                                       control_block_size=control_block_size)
        self.thread_ready.emit(thread_worker)

    def _action_gen_keys_clicked(self) -> None:
        """Method for generating keys."""
        key_size = self.ui.spin_box_key_size.value()
        private_key, public_key = RSA.gen_keys(key_size)

        self.ui.line_edit_private_key.setText(hex(private_key.d)[2:])
        self.ui.line_edit_public_key.setText(hex(public_key.e)[2:])
        self.ui.line_edit_module.setText(hex(public_key.n)[2:])

    def _action_gen_keys_from_p_q_clicked(self) -> None:
        """Method for generating keys according to the entered/generated P and Q."""
        if not self.ui.line_edit_p.text() and not self.ui.line_edit_q.text():
            QMessageBox.warning(self, "Warning!", "It is necessary to generate P and Q!")
            return

        try:
            p = int(self.ui.line_edit_p.text(), 16)
            q = int(self.ui.line_edit_q.text(), 16)
        except ValueError:
            QMessageBox.warning(self, "Warning!", "P and Q must be in hexadecimal.")
            return

        if not (isprime(p) and isprime(q)):
            QMessageBox.warning(self, "Warning!", "P and Q must be prime numbers!")
            return

        private_key, public_key = RSA.gen_keys(p=p, q=q)
        self.ui.line_edit_private_key.setText(hex(private_key.d)[2:])
        self.ui.line_edit_public_key.setText(hex(public_key.e)[2:])
        self.ui.line_edit_module.setText(hex(public_key.n)[2:])

    def _action_gen_p_q_clicked(self):
        """Method for generating prime numbers P and Q, of given dimension"""
        key_size = self.ui.spin_box_key_size.value()
        p = gen_prime(key_size)
        q = gen_prime(key_size)

        self.ui.line_edit_p.setText(hex(p)[2:])
        self.ui.line_edit_q.setText(hex(q)[2:])

    def _action_save_key_clicked(self):
        """Method for storing keys."""
        module = self.ui.line_edit_module.text()
        private_key = self.ui.line_edit_private_key.text()
        public_key = self.ui.line_edit_public_key.text()

        if not (module and private_key and public_key):
            QMessageBox.warning(self, "Warning!", "Key fields must not be empty!")
            return

        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save a key file",
            directory="",
            filter="All files (*)",
            initialFilter="All files (*)"
        )

        if not filename:
            return

        data = {
            "module": module,
            "private_key": private_key,
            "public_key": public_key
        }

        try:
            with open(filename, "w") as ofile:
                ofile.write(json.dumps(data))

        except OSError:
            QMessageBox.warning(self, "Warning!", "Failed to save file!")
            return

    def _action_load_key_clicked(self):
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

        self.ui.line_edit_module.setText(data.get("module", ""))
        self.ui.line_edit_private_key.setText(data.get("private_key", ""))
        self.ui.line_edit_public_key.setText(data.get("public_key", ""))

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file
