# This module contains the implementation of the widget for working
# with the Diffie-Hellman protocol.
from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QMenu
)

from app.crypto.protocols import DiffieHellman
from .diffie_hellman_ui import Ui_DiffieHellman


class DiffieHellmanWidget(QWidget):
    def __init__(self) -> None:
        """DiffieHellmanWidget class constructor"""
        super(DiffieHellmanWidget, self).__init__()
        self.ui = Ui_DiffieHellman()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Diffie-Hellman protocol"

        # Dictionary for storing virtual user data (ID - DiffieHellman object)
        self._users = {}

        # Context menu
        menu = QMenu()
        menu.addAction("Generate keys", self._action_gen_shared_keys_clicked)
        menu.addSeparator()
        menu.addAction("Create user", self._action_create_user_clicked)
        menu.addAction("Delete user", self._action_delete_user_clicked)

        self.ui.button_options.setMenu(menu)

        self.ui.combo_box_user.currentTextChanged.connect(self._combo_box_user_text_changed)
        self.ui.button_analysis.clicked.connect(self._button_make_clicked)

    def _button_make_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        if len(self._users) < 2:
            QMessageBox.warning(self, "Warning!", "Create 2 or more users!")
            return

        g = self.ui.line_edit_public_key_g.text()
        p = self.ui.line_edit_public_key_p.text()

        if not (g and p):
            QMessageBox.warning(self, "Warning!", "Shared public key fields must not be empty!")
            return

        try:
            int(g, 16)
            int(p, 16)
        except ValueError:
            QMessageBox.warning(self, "Warning!", "G and p keys must be in hexadecimal.")
            return

        self.ui.text_edit_stats.setText("")

        self.ui.text_edit_stats.append("Shared public keys:")
        self.ui.text_edit_stats.append(f"g: {g}")
        self.ui.text_edit_stats.append(f"p: {p}\n")
        user_ids = tuple(self._users.keys())

        for i in range(len(self._users)):
            # i - the user for whom the shared private key will be generated.
            # start_person_idx - user who will start generating the key.
            if i == 0:
                start_person_idx = 1
            else:
                start_person_idx = 0

            self.ui.text_edit_stats.append(f"Generating a shared private key for user {user_ids[i]}:")

            # We take the public key of the initial user to create intermediate keys.
            k = self._users[user_ids[start_person_idx]].public_key

            for j in range(len(self._users)):
                if i == j or j == start_person_idx:
                    continue

                # Getting an intermediate key
                k = self._users[user_ids[j]].create_intermediate_key(k)
                self.ui.text_edit_stats.append(f" - User {user_ids[j]}: intermediate key: {k.k}")

            self.ui.text_edit_stats.append("")

            # Create and set a private shared key
            self._users[user_ids[i]].create_shared_private_key(k)
            shared_private_key = self._users[user_ids[i]].shared_private_key.k
            self.ui.text_edit_stats.append(f"Final private key for user {i + 1}: {hex(shared_private_key)[2:]}\n")

    def _action_gen_shared_keys_clicked(self) -> None:
        """Method for generating public keys."""
        key_size = self.ui.spin_box_key_size.value()
        shared_keys = DiffieHellman.gen_shared_keys(key_size)
        self.ui.line_edit_public_key_g.setText(hex(shared_keys.g)[2:])
        self.ui.line_edit_public_key_p.setText(hex(shared_keys.p)[2:])

    def _action_create_user_clicked(self) -> None:
        """Method for creating virtual users."""
        DH = DiffieHellman
        g = self.ui.line_edit_public_key_g.text()
        p = self.ui.line_edit_public_key_p.text()

        if not (g and p):
            QMessageBox.warning(self, "Warning!", "Shared public key fields must not be empty!")
            return

        try:
            g = int(g, 16)
            p = int(p, 16)
        except ValueError:
            QMessageBox.warning(self, "Warning!", "Public, private keys and module must be in hexadecimal.")
            return

        shared_keys = DH.SharedKeys(g, p)
        protocol = DH(*DH.gen_keys(shared_keys), shared_keys)

        user_id = 1
        while user_id in self._users:
            user_id += 1

        self._users[user_id] = protocol
        self.ui.combo_box_user.addItem(f"User {user_id}")

    def _action_delete_user_clicked(self) -> None:
        """Method for deleting virtual user."""
        if not self._users:
            return

        current_text = self.ui.combo_box_user.currentText()
        current_index = self.ui.combo_box_user.currentIndex()
        user_id = int(current_text.split()[1])
        del self._users[user_id]
        self.ui.combo_box_user.removeItem(current_index)

    def _combo_box_user_text_changed(self, data: str) -> None:
        """Method for handling widget changes with virtual users."""
        if not data:
            self.ui.line_edit_public_key.setText("")
            self.ui.line_edit_private_key.setText("")
            return

        user_id = int(data.split()[1])
        protocol = self._users.get(user_id)

        self.ui.line_edit_public_key.setText(hex(protocol.public_key.k))
        self.ui.line_edit_private_key.setText(hex(protocol.private_key.k))
