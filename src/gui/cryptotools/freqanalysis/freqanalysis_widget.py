from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog
)
from PyQt6.QtCore import (
    Qt,
    QUrl
)
import pyqtgraph as pg

from .freqanalysis_ui import Ui_freqanalysis
from src.gui.widgets import DragDropWidget
from src.gui.const import (
    FREQ_ANALYSIS_SUPPORT_EXT,
    MAX_CHARS_READ
)
from src.crypto.tools import (
    freqanalysis as fa
)


class FreqAnalysisWidget(QWidget):
    def __init__(self):
        super(FreqAnalysisWidget, self).__init__()
        self.ui = Ui_freqanalysis()
        self.ui.setupUi(self)

        self.title = "Frequency cryptanalysis"
        self.current_lang = "english"

        self.file_path = QUrl()

        self.freq_text = {}
        self.freq_table = {}
        # letter from text: letter from table
        self.letter_match = {}

        # Add Drag and drop widget
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(FREQ_ANALYSIS_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Init plot
        self.plot = pg.PlotWidget()
        self.plot.addLegend()
        self.plot.setBackground("white")
        layout = QVBoxLayout(self.ui.group_box_graph)
        layout.addWidget(self.plot)
        layout.setContentsMargins(0, 0, 0, 0)

        self.bar_graph_freq_text = pg.BarGraphItem(
            x=[0],
            height=[0],
            width=0.5,
            brush=(83, 142, 242, 150),
            name="Input text frequency table"
        )
        self.bar_graph_freq_table = pg.BarGraphItem(
            x=[0],
            height=[0],
            width=0.5,
            brush=(33, 33, 33, 50),
            name="Sample frequency table"
        )
        self.plot.addItem(self.bar_graph_freq_text)
        self.plot.addItem(self.bar_graph_freq_table)

        # table match
        self.ui.match_table_widget.horizontalHeader().setStretchLastSection(True)

        self.ui.button_analysis.clicked.connect(self.button_analysis_clicked)
        self.ui.button_dechipher.clicked.connect(self.button_decipher_clicked)

        self.ui.match_table_widget.itemChanged.connect(self.freq_table_item_changed)

        self.drag_drop_widget.dropped.connect(self.file_path_changed)
        self.drag_drop_widget.canceled.connect(self.file_path_changed)

        self.ui.combo_box_text_style.currentTextChanged.connect(self.text_style_changed)

    def button_analysis_clicked(self):
        self.current_lang = self.ui.combo_box_lang.currentText().lower()
        self.freq_table = fa.get_freq_table(
            lang=self.current_lang.lower(),
            text_type=self.ui.combo_box_text_style.currentText().lower()
        )
        self.update_bar_graph(self.bar_graph_freq_table, self.freq_table)
        self.plot.getAxis("bottom").setTicks([list(enumerate(self.freq_table.keys()))])

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                try:
                    self.freq_text = fa.analysis(
                        text=self.ui.text_edit_input.toPlainText().lower(),
                        freq_table=self.freq_table
                    )
                except fa.FreqAnalysisError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

            case self.ui.tab_document:
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                try:
                    # clear
                    self.freq_text.clear()

                    with open(self.file_path.toLocalFile(), "r") as file:
                        while block := file.read(MAX_CHARS_READ):
                            freq_table = fa.analysis(
                                text=block.lower(),
                                freq_table=self.freq_table
                            )

                            if not self.freq_text:
                                self.freq_text = freq_table
                                continue

                            for key, value in freq_table.items():
                                self.freq_text[key] += value

                except fa.FreqAnalysisError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

                except OSError:
                    QMessageBox.warning(self, "Warning!", "Error while reading or writing to file!")
                    return

            case _:
                return

        num_of_letters = sum(self.freq_text.values())
        for key in self.freq_text.keys():
            self.freq_text[key] = self.freq_text[key] / num_of_letters * 100

        self.update_bar_graph(self.bar_graph_freq_text, self.freq_text)
        self.update_table_match()

    def button_decipher_clicked(self):
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                try:
                    self.ui.text_edit_output.setText(
                        fa.decipher(
                            text=self.ui.text_edit_input.toPlainText(),
                            letter_match=self.letter_match
                        )
                    )

                except fa.FreqAnalysisError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

            case self.ui.tab_document:
                if self.file_path.isEmpty():
                    QMessageBox.warning(self, "Warning!", "File not selected!")
                    return

                # get the name of the new file
                file_path_output, _ = QFileDialog.getSaveFileName(
                    parent=self,
                    caption="Save new file",
                    directory="",
                    filter=FREQ_ANALYSIS_SUPPORT_EXT,
                )

                if not file_path_output:
                    return

                # Attempt to open input file
                try:
                    file_input = open(self.file_path.toLocalFile(), "r")

                except OSError:
                    QMessageBox.warning(self, "Warning!", "Error opening input file!")
                    return

                # Attempt to open output file
                try:
                    file_output = open(file_path_output, "w")

                except OSError:
                    # Closing the input file
                    file_input.close()
                    QMessageBox.warning(self, "Warning!", "Error opening output file!")
                    return

                try:
                    while block := file_input.read(MAX_CHARS_READ):
                        processed_block = fa.decipher(
                            text=block,
                            letter_match=self.letter_match
                        )
                        file_output.write(processed_block)

                except fa.FreqAnalysisError as e:
                    QMessageBox.warning(self, "Warning!", e.args[0])
                    return

                except OSError:
                    QMessageBox.warning(self, "Warning!", "An error occurred while writing to file!")
                    return

                finally:
                    file_input.close()
                    file_output.close()

            case _:
                return

    @staticmethod
    def update_bar_graph(graph: pg.BarGraphItem, freq_table: dict):
        graph.setOpts(
            x=range(len(freq_table.keys())),
            height=list(freq_table.values())
        )

    def update_table_match(self):
        text_letter_sorted = tuple(letter for letter, freq in sorted(
            self.freq_text.items(), key=lambda x: x[1], reverse=True
        ))
        table_letter_sorted = tuple(letter for letter, freq, in sorted(
            self.freq_table.items(), key=lambda x: x[1], reverse=True
        ))

        letter_match = {text_letter: table_letter for text_letter, table_letter in zip(
            text_letter_sorted,
            table_letter_sorted
        )}

        self.letter_match = dict.fromkeys(self.freq_table.keys())
        self.letter_match.update(letter_match)

        self.ui.match_table_widget.blockSignals(True)
        self.ui.match_table_widget.setRowCount(len(self.letter_match))
        self.ui.match_table_widget.setVerticalHeaderLabels(self.letter_match.keys())
        self.ui.match_table_widget.setColumnCount(1)
        self.ui.match_table_widget.horizontalHeader().hide()

        for i, (text_letter, table_letter) in enumerate(self.letter_match.items()):
            item = QTableWidgetItem(table_letter)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.match_table_widget.setItem(i, 0, item)
        self.ui.match_table_widget.blockSignals(False)

    def freq_table_item_changed(self, item: QTableWidgetItem):
        current_row_label = self.ui.match_table_widget.verticalHeaderItem(item.row()).text()
        current_text_letter = self.letter_match.get(current_row_label)

        self.ui.match_table_widget.blockSignals(True)
        if item.text().lower() not in self.letter_match.keys():
            item.setText(current_text_letter)
            self.ui.match_table_widget.blockSignals(False)
            return

        item.setText(item.text().lower())

        other_table_letter_index = tuple(self.letter_match.values()).index(item.text())
        other_text_letter = tuple(self.letter_match.keys())[other_table_letter_index]

        table_match_index = tuple(self.freq_table.keys()).index(other_text_letter)
        other_item = self.ui.match_table_widget.item(table_match_index, 0)
        other_item.setText(current_text_letter)
        self.ui.match_table_widget.blockSignals(False)

        self.letter_match.update({
            current_row_label: self.letter_match[other_text_letter],
            other_text_letter: self.letter_match[current_row_label]
        })
        self.freq_text.update({
            current_row_label: self.freq_text[other_text_letter],
            other_text_letter: self.freq_text[current_row_label]
        })

        self.update_bar_graph(self.bar_graph_freq_text, self.freq_text)

    def file_path_changed(self, file: QUrl):
        self.file_path = file

    def text_style_changed(self, text_style: str):
        self.freq_table = fa.get_freq_table(
            lang=self.current_lang.lower(),
            text_type=text_style.lower()
        )
        self.update_bar_graph(self.bar_graph_freq_table, self.freq_table)
        self.update_table_match()
