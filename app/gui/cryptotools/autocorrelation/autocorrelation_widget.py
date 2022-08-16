from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import QUrl

from .autocorrelation_ui import Ui_Autocorrelation
from app.crypto.tools.autocorrelation import (
    Autocorrelation,
    AutocorrError
)
from app.crypto.const import ALPHABET_TABLE
from app.gui.widgets import DragDropWidget
from app.gui.const import (
    AUTOCORRELATION_SUPPORT_EXT,
    MAX_CHARS_READ
)


class AutocorrelationWidget(QWidget):
    def __init__(self):
        super(AutocorrelationWidget, self).__init__()
        self.ui = Ui_Autocorrelation()
        self.ui.setupUi(self)

        self.title = "Autocorrelation method"

        self.file_path = QUrl()

        # Init languages
        self.ui.combo_box_lang.addItems(map(lambda x: x.capitalize(), ALPHABET_TABLE.keys()))

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(AUTOCORRELATION_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

        self.ui.button_analysis.clicked.connect(self._button_analysis_clicked)
        self.ui.check_box_custom_key_length.stateChanged.connect(self._check_box_check)

        self._check_box_check()

    def _button_analysis_clicked(self):
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
            crypto_tool = Autocorrelation(text, max_key_length, delta, lang)

            if self.ui.check_box_custom_key_length.isChecked():
                key_length = self.ui.spin_box_custom_key_length.value()
                self.ui.text_edit_stats.append(f"Key length: {key_length} (custom)\n")

            else:
                key_length = crypto_tool.find_possible_key_length()
                self.ui.text_edit_stats.append(f"Key length: {key_length} (possible)\n")

            possible_key = crypto_tool.find_possible_key(key_length)
            self.ui.text_edit_stats.append(f"Possible key: \"{possible_key}\"")

        except AutocorrError as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

    def _check_box_check(self) -> None:
        if self.ui.check_box_custom_key_length.isChecked():
            self.ui.spin_box_custom_key_length.setDisabled(False)
            self.ui.check_box_custom_key_length.setStyleSheet("color: palette(window-text)")
        else:
            self.ui.spin_box_custom_key_length.setDisabled(True)
            self.ui.check_box_custom_key_length.setStyleSheet("color: grey")

    def _file_path_changed(self, file: QUrl):
        self.file_path = file
