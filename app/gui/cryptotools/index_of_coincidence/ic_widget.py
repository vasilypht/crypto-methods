# This module contains the widget implementation for the index of coincidence analysis module.
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import QUrl

from .ic_ui import Ui_IC
from app.crypto.tools import IndexOfCoincidence
from app.crypto.exceptions import ICError
from app.crypto.common import Languages
from app.gui.widgets import DragDropWidget
from app.gui.const import (
    IC_SUPPORT_EXT,
    MAX_CHARS_READ
)


class ICWidget(QWidget):
    def __init__(self) -> None:
        """ICWidget class constructor"""
        super(ICWidget, self).__init__()
        self.ui = Ui_IC()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Index of coincidence"

        # Path received from dragdrop widget
        self.file_path = QUrl()

        # Init languages
        self.ui.combo_box_lang.addItems((lang.name.capitalize() for lang in Languages))

        # Create a dragdrop widget and place it on the document tab.
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(IC_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

        self.ui.button_analysis.clicked.connect(self._button_analysis_clicked)
        self.ui.check_box_custom_key_length.stateChanged.connect(self._check_box_check)

        self._check_box_check()

    def _button_analysis_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        self.ui.text_edit_stats.clear()

        lang = Languages.from_str(self.ui.combo_box_lang.currentText())
        delta = self.ui.double_spin_box_delta.value()
        max_key_length = self.ui.spin_box_max_key_length.value()

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                text = self.ui.text_edit_input.toPlainText()[:MAX_CHARS_READ]

            case self.ui.tab_document:
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                try:
                    with open(self.file_path.toLocalFile(), "r") as file:
                        text = file.read(MAX_CHARS_READ)

                except OSError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

            case _:
                return

        try:
            crypto_tool = IndexOfCoincidence(text, max_key_length, delta, lang)

            # Search for a key value given a length value by the user.
            if self.ui.check_box_custom_key_length.isChecked():
                key_length = self.ui.spin_box_custom_key_length.value()
                self.ui.text_edit_stats.append(f"Key length: {key_length} (custom)\n")

            else:
                # We are looking for the probable key length.
                key_length = crypto_tool.find_possible_key_length()
                self.ui.text_edit_stats.append(f"Key length: {key_length} (possible)\n")

            possible_keys = crypto_tool.find_possible_keys(key_length)
            self.ui.text_edit_stats.append(f"Possible keys ({len(possible_keys)}):")
            for key in possible_keys:
                self.ui.text_edit_stats.append(f" -> \"{key}\"")

        except ICError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

    def _check_box_check(self) -> None:
        """Method for activating/deactivating a spinbox."""
        if self.ui.check_box_custom_key_length.isChecked():
            self.ui.spin_box_custom_key_length.setDisabled(False)
            self.ui.check_box_custom_key_length.setStyleSheet("color: palette(window-text)")
        else:
            self.ui.spin_box_custom_key_length.setDisabled(True)
            self.ui.check_box_custom_key_length.setStyleSheet("color: grey")

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file
