from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import QUrl

from .ic_ui import Ui_ic
from app.crypto.tools.index_of_coincidence import (
    IndexOfCoincidence,
    ICError
)
from app.crypto.const import ALPHABET_TABLE
from app.gui.widgets import DragDropWidget
from app.gui.const import (
    IC_SUPPORT_EXT,
    MAX_CHARS_READ
)


class ICWidget(QWidget):
    def __init__(self):
        super(ICWidget, self).__init__()
        self.ui = Ui_ic()
        self.ui.setupUi(self)

        self.title = "Index of coincidence"

        self.file_path = QUrl()

        # Init languages
        self.ui.combo_box_lang.addItems(map(lambda x: x.capitalize(), ALPHABET_TABLE.keys()))

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(IC_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        self.drag_drop_widget.dropped.connect(self.file_path_changed)
        self.drag_drop_widget.canceled.connect(self.file_path_changed)

        self.ui.button_analysis.clicked.connect(self.button_analysis_clicked)
        self.ui.check_box_custom_key_length.stateChanged.connect(self.check_box_check)

        self.check_box_check()

    def button_analysis_clicked(self):
        self.ui.text_edit_stats.clear()

        lang = self.ui.combo_box_lang.currentText().lower()
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
            ic = IndexOfCoincidence(
                text=text,
                max_len=max_key_length,
                delta=delta,
                lang=lang
            )

            if self.ui.check_box_custom_key_length.isChecked():
                key_length = self.ui.spin_box_custom_key_length.value()
                self.ui.text_edit_stats.append(f"Key length: {key_length} (custom)\n")

            else:
                key_length = ic.find_possible_key_length()
                self.ui.text_edit_stats.append(f"Key length: {key_length} (possible)\n")

            possible_keys = ic.find_possible_keys(key_length)
            self.ui.text_edit_stats.append(f"Possible keys ({len(possible_keys)}):")
            for key in possible_keys:
                self.ui.text_edit_stats.append(f" -> \"{key}\"")

        except ICError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

    def check_box_check(self) -> None:
        if self.ui.check_box_custom_key_length.isChecked():
            self.ui.spin_box_custom_key_length.setDisabled(False)
            self.ui.check_box_custom_key_length.setStyleSheet("color: palette(window-text)")
        else:
            self.ui.spin_box_custom_key_length.setDisabled(True)
            self.ui.check_box_custom_key_length.setStyleSheet("color: grey")

    def file_path_changed(self, file: QUrl):
        self.file_path = file
