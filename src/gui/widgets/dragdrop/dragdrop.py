import re

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QFileDialog
)
from PyQt6.QtCore import (
    QFileInfo,
    pyqtSignal,
    QUrl
)
from PyQt6.QtGui import (
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QPixmap
)

from .selected_file_widget_ui import Ui_SelectedFileWidget
from .dragdrop_upload_widget_ui import Ui_DragDropUploadWidget


class DragDropUploadWidget(QWidget):
    dropped = pyqtSignal(QUrl)

    def __init__(self, *args, **kwargs):
        super(DragDropUploadWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_DragDropUploadWidget()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        self.filter_extensions = "Text files (*.txt)"
        self.extensions = ("txt",)

        self.ui.button_dragdrop.clicked.connect(self.action_clicked_choose_file)

    def action_clicked_choose_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a key file",
            directory="",
            filter=self.filter_extensions,
        )

        if not filename:
            return

        self.dropped.emit(QUrl.fromLocalFile(filename))

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            file_ext = QFileInfo(file_path).completeSuffix()

            if file_ext in self.extensions:
                event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            file_ext = QFileInfo(file_path).completeSuffix()

            if file_ext in self.extensions:
                event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            file = event.mimeData().urls()[0]
            self.dropped.emit(file)
            event.accept()
        else:
            event.ignore()


class SelectedFileWidget(QWidget):
    canceled = pyqtSignal(QUrl)

    def __init__(self, *args, **kwargs):
        super(SelectedFileWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_SelectedFileWidget()
        self.ui.setupUi(self)
        self.ui.label_icon.setPixmap(QPixmap("icons:file.png").scaled(32, 32))
        self.ui.button_close.clicked.connect(lambda: self.canceled.emit(QUrl()))


class DragDropWidget(QWidget):
    dropped = pyqtSignal(QUrl)
    canceled = pyqtSignal(QUrl)

    def __init__(self, *args, **kwargs):
        super(DragDropWidget, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.resize(400, 200)

        self.file_path = ""

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget = QStackedWidget(self)
        layout.addWidget(self.stacked_widget)

        self.widget_dragdrop = DragDropUploadWidget()
        self.widget_loadedfile = SelectedFileWidget()

        self.stacked_widget.addWidget(self.widget_dragdrop)
        self.stacked_widget.addWidget(self.widget_loadedfile)

        self.stacked_widget.setCurrentWidget(self.widget_dragdrop)

        self.widget_loadedfile.canceled.connect(self.canceled_file)
        self.widget_dragdrop.dropped.connect(self.dropped_file)
        
    def set_filter_extensions(self, extensions: str):
        ext_array = re.findall(r"(\*\.[\da-z]+)+", extensions, re.IGNORECASE)
        ext_array = tuple(map(lambda s: s[2::], ext_array))
        self.widget_dragdrop.extensions = ext_array
        self.widget_dragdrop.filter_extensions = extensions

    def dropped_file(self, file: QUrl):
        self.widget_loadedfile.ui.label_file.setText(file.fileName())
        self.stacked_widget.setCurrentWidget(self.widget_loadedfile)
        self.dropped.emit(file)

    def canceled_file(self, file: QUrl):
        self.stacked_widget.setCurrentWidget(self.widget_dragdrop)
        self.canceled.emit(file)
