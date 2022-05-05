from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import QUrl

from .kasiski_ui import Ui_kasiski
from src.crypto.tools.kasiski import Kasiski
from src.gui.widgets import DragDropWidget
from src.gui.const import (
    KASISKI_SUPPORT_EXT,
    MAX_CHARS_READ
)


class KasiskiWidget(QWidget):
    def __init__(self):
        super(KasiskiWidget, self).__init__()
        self.ui = Ui_kasiski()
        self.ui.setupUi(self)

        self.title = "Kasiski examination"

        self.file_path = QUrl()

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(KASISKI_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        self.drag_drop_widget.dropped.connect(self.file_path_changed)
        self.drag_drop_widget.canceled.connect(self.file_path_changed)

        self.ui.button_analysis.clicked.connect(self.button_analysis_clicked)

    def button_analysis_clicked(self):
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

        kasiski = Kasiski(
            text=text,
            seq_len=seq_len,
            threshold=threshold,
            min_len=min_key_length,
            max_len=max_key_length
        )

        lengths = kasiski.find_possible_key_lengths()

        self.ui.text_edit_stats.append(f"Found lengths: {len(lengths)}")
        self.ui.text_edit_stats.append(f"Possible key lengths:")
        self.ui.text_edit_stats.append(f"{lengths}")

    def file_path_changed(self, file: QUrl):
        self.file_path = file
