# This module contains the widget implementation for the frequency analysis module.
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
from app.gui.widgets import DragDropWidget
from app.gui.const import (
    FREQ_ANALYSIS_SUPPORT_EXT,
    MAX_CHARS_READ
)
from app.crypto.tools import FreqAnalysis
from app.crypto.common import (
    Languages,
    TextStyle
)


class FreqAnalysisWidget(QWidget):
    def __init__(self) -> None:
        """FreqAnalysisWidget class constructor"""
        super(FreqAnalysisWidget, self).__init__()
        self.ui = Ui_freqanalysis()
        self.ui.setupUi(self)

        # Define the name of the widget that will be displayed in the list of widgets.
        self.title = "Frequency cryptanalysis"

        # Path received from dragdrop widget.
        self.file_path = QUrl()

        # Dictionary frequency formed by text.
        self.freqs_by_text = {}
        # Frequency dictionary taken from constant tables.
        self.freqs_by_table = {}

        # Replacement letter dictionary: letter from text -> letter from table.
        self.letter_match = {}

        # Init languages and styles
        self.ui.combo_box_lang.addItems((lang.name.capitalize() for lang in Languages))
        self.ui.combo_box_text_style.addItems((style.name.capitalize() for style in TextStyle))

        # Create a dragdrop widget and place it on the document tab.
        self.drag_drop_widget = DragDropWidget(self.ui.tab_document)
        self.drag_drop_widget.set_filter_extensions(FREQ_ANALYSIS_SUPPORT_EXT)
        vertical_layout = QVBoxLayout(self.ui.tab_document)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.drag_drop_widget)

        # Create and init plot
        self.plot = pg.PlotWidget()
        self.plot.addLegend()
        self.plot.setBackground("white")
        layout = QVBoxLayout(self.ui.group_box_graph)
        layout.addWidget(self.plot)
        layout.setContentsMargins(0, 0, 0, 0)

        # Graph for drawing frequencies by text.
        self.bar_graph_freqs_by_text = pg.BarGraphItem(
            x=[0],
            height=[0],
            width=0.5,
            brush=(83, 142, 242, 150),
            name="Input text frequency table"
        )

        # Graph for drawing frequencies from the table.
        self.bar_graph_freqs_by_table = pg.BarGraphItem(
            x=[0],
            height=[0],
            width=0.5,
            brush=(33, 33, 33, 50),
            name="Sample frequency table"
        )
        self.plot.addItem(self.bar_graph_freqs_by_text)
        self.plot.addItem(self.bar_graph_freqs_by_table)

        self.ui.match_table_widget.horizontalHeader().setStretchLastSection(True)

        # Associating the analysis and decryption buttons with the corresponding slots.
        self.ui.button_analysis.clicked.connect(self._button_analysis_clicked)
        self.ui.button_dechipher.clicked.connect(self._button_decipher_clicked)

        self.ui.match_table_widget.itemChanged.connect(self._freq_table_item_changed)

        # Binds to get the path to the file that is dropped into the widget
        # and remove the path when the file is removed from the widget.
        self.drag_drop_widget.dropped.connect(self._file_path_changed)
        self.drag_drop_widget.canceled.connect(self._file_path_changed)

        self.ui.combo_box_text_style.currentTextChanged.connect(self._text_style_changed)

    def _button_analysis_clicked(self) -> None:
        """Method - a slot for processing a signal when a button is pressed."""
        # We read the given language, get the table of frequencies
        # of this language and draw a graph
        self.current_lang = Languages.from_str(self.ui.combo_box_lang.currentText())
        self.freqs_by_table = FreqAnalysis.get_freq_table(
            lang=self.current_lang,
            text_type=TextStyle.from_str(self.ui.combo_box_text_style.currentText())
        )
        self.update_bar_graph(self.bar_graph_freqs_by_table, self.freqs_by_table)
        self.plot.getAxis("bottom").setTicks([list(enumerate(self.freqs_by_table.keys()))])

        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_analysis_processing()

            case self.ui.tab_document:
                self._tab_document_analysis_processing()

            case _:
                return

        # Converting frequencies to probabilities
        num_of_letters = sum(self.freqs_by_text.values())
        for key in self.freqs_by_text.keys():
            self.freqs_by_text[key] = self.freqs_by_text[key] / num_of_letters * 100

        # Draw a graph of frequencies by text
        self.update_bar_graph(self.bar_graph_freqs_by_text, self.freqs_by_text)
        # Update widget and letter matching dictionary.
        self.update_table_match()

    def _tab_text_analysis_processing(self) -> None:
        """Method for processing from the widget for working with text."""
        data = self.ui.text_edit_input.toPlainText().lower()

        try:
            self.freqs_by_text = FreqAnalysis.analysis(data, self.freqs_by_table)

        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

    def _tab_document_analysis_processing(self) -> None:
        """Method for processing from a widget for working with a file."""
        if self.file_path.isEmpty():
            QMessageBox.warning(self, "Warning!", "File not selected!")
            return

        try:
            self.freqs_by_text.clear()

            with open(self.file_path.toLocalFile(), "r") as file:
                while block := file.read(MAX_CHARS_READ):
                    freq_table = FreqAnalysis.analysis(block.lower(), self.freqs_by_table)

                    # If the dictionary is empty, then we initialize it with a new value.
                    if not self.freqs_by_text:
                        self.freqs_by_text = freq_table
                        continue

                    # Adding new values to the dictionary.
                    for key, value in freq_table.items():
                        self.freqs_by_text[key] += value

        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        except OSError:
            QMessageBox.warning(self, "Warning!", "Error while reading or writing to file!")
            return

    def _button_decipher_clicked(self) -> None:
        """Method - a slot for signal processing when the decipher button is pressed."""
        match self.ui.tab_widget.currentWidget():
            case self.ui.tab_text:
                self._tab_text_decipher_processing()

            case self.ui.tab_document:
                self._tab_document_decipher_processing()

            case _:
                return

    def _tab_text_decipher_processing(self) -> None:
        """Method for processing from the widget for working with text. (decipher)"""
        data = self.ui.text_edit_input.toPlainText()

        try:
            processed_data = FreqAnalysis.decipher(data, self.letter_match)

        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

        self.ui.text_edit_output.setText(processed_data)

    def _tab_document_decipher_processing(self) -> None:
        """Method for processing from a widget for working with a file. (decipher)"""
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

        try:
            with open(self.file_path.toLocalFile(), "r") as input_file, \
                    open(file_path_output, "w") as output_file:
                while block := input_file.read(MAX_CHARS_READ):
                    processed_block = FreqAnalysis.decipher(block, self.letter_match)
                    output_file.write(processed_block)

        except OSError:
            QMessageBox.warning(self, "Warning!", "Error opening input/output file!")
            return

        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "Warning!", e.args[0])
            return

    @staticmethod
    def update_bar_graph(graph: pg.BarGraphItem, freq_table: dict) -> None:
        """Method for updating bar graph."""
        graph.setOpts(
            x=range(len(freq_table.keys())),
            height=list(freq_table.values())
        )

    def update_table_match(self) -> None:
        """Method for updating the replacement letter mapping table."""
        # Sort the text frequency table by frequency.
        text_letter_sorted = tuple(letter for letter, freq in sorted(
            self.freqs_by_text.items(), key=lambda x: x[1], reverse=True
        ))
        # Sort the constant frequency table by frequency.
        table_letter_sorted = tuple(letter for letter, freq, in sorted(
            self.freqs_by_table.items(), key=lambda x: x[1], reverse=True
        ))

        # Compiling a dictionary of matching letters sorted by frequency.
        letter_match = {text_letter: table_letter for text_letter, table_letter in zip(
            text_letter_sorted,
            table_letter_sorted
        )}

        # Compiling a dictionary with the keys in alphabetical order.
        self.letter_match = dict.fromkeys(self.freqs_by_table.keys())
        self.letter_match.update(letter_match)

        # We block the widget's signal so that another method does
        # not work. We initialize the column and rows.
        self.ui.match_table_widget.blockSignals(True)
        self.ui.match_table_widget.setRowCount(len(self.letter_match))
        self.ui.match_table_widget.setVerticalHeaderLabels(self.letter_match.keys())
        self.ui.match_table_widget.setColumnCount(1)
        self.ui.match_table_widget.horizontalHeader().hide()

        # Fill in the rows of the table widget.
        for i, (text_letter, table_letter) in enumerate(self.letter_match.items()):
            item = QTableWidgetItem(table_letter)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.match_table_widget.setItem(i, 0, item)

        self.ui.match_table_widget.blockSignals(False)

    def _freq_table_item_changed(self, item: QTableWidgetItem) -> None:
        """A method for handling a change in a value in a table."""
        # We get the title of the line in which the change took place.
        # Next, we get from the table the letter that corresponds to the title.
        current_row_label = self.ui.match_table_widget.verticalHeaderItem(item.row()).text()
        current_text_letter = self.letter_match.get(current_row_label)

        # If the changed value is not in the mapping table, then we change
        # the value to the old one.
        self.ui.match_table_widget.blockSignals(True)
        if item.text().lower() not in self.letter_match.keys():
            item.setText(current_text_letter)
            self.ui.match_table_widget.blockSignals(False)
            return

        # If there is such a value in the table, then we translate it into lowercase.
        item.setText(item.text().lower())

        # Next, the key is found, which corresponds to the new value entered by the user.
        other_table_letter_index = tuple(self.letter_match.values()).index(item.text())
        other_text_letter = tuple(self.letter_match.keys())[other_table_letter_index]

        # We get the item of the new letter, and put the old value there.
        other_item = self.ui.match_table_widget.item(other_table_letter_index, 0)
        other_item.setText(current_text_letter)
        self.ui.match_table_widget.blockSignals(False)

        # We update the dictionary with frequencies.
        self.letter_match.update({
            current_row_label: self.letter_match[other_text_letter],
            other_text_letter: self.letter_match[current_row_label]
        })
        self.freqs_by_text.update({
            current_row_label: self.freqs_by_text[other_text_letter],
            other_text_letter: self.freqs_by_text[current_row_label]
        })

        # We redraw the graph of frequencies according to the text.
        self.update_bar_graph(self.bar_graph_freqs_by_text, self.freqs_by_text)

    def _file_path_changed(self, file: QUrl) -> None:
        """Method - a slot for processing a signal from the dragdrop widget to get the path to the file."""
        self.file_path = file

    def _text_style_changed(self, text_style: str) -> None:
        """The method is a slot to handle changing the text style value."""
        # We get a new table of frequencies corresponding to
        # the text style, and draw it.
        self.freqs_by_table = FreqAnalysis.get_freq_table(
            lang=self.current_lang,
            text_type=TextStyle.from_str(text_style)
        )
        self.update_bar_graph(self.bar_graph_freqs_by_table, self.freqs_by_table)
        self.update_table_match()
