# This module contains the implementation of the widget for working
# with the Shamir protocol.
from random import randrange

from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QMenu
)

from app.crypto.protocols import Shamir
from app.crypto.utils import gen_prime
from .shamir_ui import Ui_Shamir


class ShamirWidget(QWidget):
    def __init__(self) -> None:
        """ShamirWidget class constructor"""
        super(ShamirWidget, self).__init__()
        self.ui = Ui_Shamir()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Three-step Shamir protocol"

        # Context menu
        menu = QMenu()
        menu.addAction("Generate key p", self._action_gen_key_p_clicked)
        menu.addAction("Generate a key for Alice", self._action_gen_key_alice_clicked)
        menu.addAction("Generate a key for Bob", self._action_gen_key_bob_clicked)

        self.ui.button_options.setMenu(menu)

        self.ui.button_make.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        p = self.ui.line_edit_public_key_p.text()

        alice_pb_key = self.ui.line_edit_alice_public_key.text()
        alice_pr_key = self.ui.line_edit_alice_private_key.text()

        bob_pb_key = self.ui.line_edit_bob_public_key.text()
        bob_pr_key = self.ui.line_edit_bob_private_key.text()

        if not (p and alice_pr_key and alice_pb_key and bob_pr_key and bob_pb_key):
            QMessageBox.warning(self, "Warning!", "All fields must be filled!")
            return

        try:
            p = int(p, 16)

            alice_pb_key = Shamir.PublicKey(int(alice_pb_key, 16), p)
            alice_pr_key = Shamir.PrivateKey(int(alice_pr_key, 16), p)

            bob_pb_key = Shamir.PublicKey(int(bob_pb_key, 16), p)
            bob_pr_key = Shamir.PrivateKey(int(bob_pr_key, 16), p)
        except ValueError:
            QMessageBox.warning(self, "Warning!", "All fields must be in hexadecimal format.")
            return

        self.ui.text_edit_stats.setText("")

        self.ui.text_edit_stats.append("Shared public key:")
        self.ui.text_edit_stats.append(f"p: {self.ui.line_edit_public_key_p.text()}\n")

        alice_protocol = Shamir(alice_pr_key, alice_pb_key)
        bob_protocol = Shamir(bob_pr_key, bob_pb_key)

        data = randrange(2, p)

        self.ui.text_edit_stats.append(f"Message: {hex(data)}\n")

        self.ui.text_edit_stats.append("Transfer start.\n")

        self.ui.text_edit_stats.append("--- Alice encrypts the message with the 'public key'. ---")
        encrypted_data = alice_protocol.encrypt(data)
        self.ui.text_edit_stats.append(f"Encrypted data: {hex(encrypted_data)}\n")

        self.ui.text_edit_stats.append("--- Alice sends a message to Bob. ---\n")
        self.ui.text_edit_stats.append("--- Bob encrypts the message with the 'public key'. ---")
        encrypted_data = bob_protocol.encrypt(encrypted_data)
        self.ui.text_edit_stats.append(f"Encrypted data: {hex(encrypted_data)}\n")

        self.ui.text_edit_stats.append("--- Bob sends a message to Alice. ---\n")
        self.ui.text_edit_stats.append("--- Alice decrypts the message with her 'private key'. ---")
        decrypted_data = alice_protocol.decrypt(encrypted_data)
        self.ui.text_edit_stats.append(f"Decrypted data: {hex(decrypted_data)}\n")

        self.ui.text_edit_stats.append("--- Alice sends a message to Bob. ---\n")
        self.ui.text_edit_stats.append("--- Bob decrypts the message with her 'private key'. ---")
        decrypted_data = bob_protocol.decrypt(decrypted_data)
        self.ui.text_edit_stats.append(f"Decrypted data: {hex(decrypted_data)}\n")

        self.ui.text_edit_stats.append("End of transmission.\n")

        self.ui.text_edit_stats.append(f"Sent message: {hex(data)}")
        self.ui.text_edit_stats.append(f"Message received: {hex(decrypted_data)}")

    def _action_gen_key_p_clicked(self) -> None:
        """The method for generating the public key - P prime number."""
        key_size = self.ui.spin_box_key_size.value()
        p = gen_prime(key_size)
        self.ui.line_edit_public_key_p.setText(hex(p)[2:])

    def _action_gen_key_alice_clicked(self) -> None:
        """Method for generating Alice's keys"""
        p = self.ui.line_edit_public_key_p.text()

        if not p:
            QMessageBox.warning(self, "Warning!", "The public key field n must not be empty!")
            return

        try:
            private_key, public_key = Shamir.gen_keys(int(p, 16))
        except ValueError:
            QMessageBox.warning(self, "Warning!", "Key p must be in hexadecimal.")
            return

        self.ui.line_edit_alice_private_key.setText(hex(private_key.k)[2:])
        self.ui.line_edit_alice_public_key.setText(hex(public_key.k)[2:])

    def _action_gen_key_bob_clicked(self) -> None:
        """Method for generating Bob's keys"""
        p = self.ui.line_edit_public_key_p.text()

        if not p:
            QMessageBox.warning(self, "Warning!", "The public key field n must not be empty!")
            return

        try:
            private_key, public_key = Shamir.gen_keys(int(p, 16))
        except ValueError:
            QMessageBox.warning(self, "Warning!", "Key p must be in hexadecimal.")
            return

        self.ui.line_edit_bob_private_key.setText(hex(private_key.k)[2:])
        self.ui.line_edit_bob_public_key.setText(hex(public_key.k)[2:])
