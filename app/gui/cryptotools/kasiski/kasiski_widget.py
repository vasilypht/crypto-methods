# This module contains the widget implementation for the Kasiski analysis module.
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import QUrl

from .kasiski_ui import Ui_kasiski
from app.crypto.tools import Kasiski
from app.gui.widgets import DragDropWidget
from app.gui.const import (
    KASISKI_SUPPORT_EXT,
    MAX_CHARS_READ
)


class KasiskiWidget(QWidget):
    def __init__(self) -> None:
        """KasiskiWidget class constructor"""
        super(KasiskiWidget, self).__init__()
        self.ui = Ui_kasiski()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Kasiski examination"

        # Path received from dragdrop widget
        self.file_path = QUrl()

        # Create a dragdrop widget and place it on the document tab.
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(KASISKI_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

        self.ui.button_analysis.clicked.connect(self._button_analysis_clicked)

    def _button_analysis_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        self.ui.text_edit_stats.clear()

        threshold = self.ui.spin_box_threshold.value()
        seq_len = self.ui.spin_box_seq_len.value()
        min_key_length = self.ui.spin_box_min_key_length.value()
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

        crypto_tool = Kasiski(text, seq_len, threshold, min_key_length, max_key_length)
        lengths = crypto_tool.find_possible_key_lengths()

        self.ui.text_edit_stats.append(f"Found lengths: {len(lengths)}")
        self.ui.text_edit_stats.append(f"Possible key lengths:")
        self.ui.text_edit_stats.append(f"{lengths}")

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file
