import shutil

from PyQt6.QtWidgets import (
    QMainWindow,
    QTreeWidgetItem,
    QWidget,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QIcon

from .mainwindow_ui import Ui_MainWindow
from .defmodules import WIDGETS_DEFAULT
from .symmetric import WIDGETS_SYMMETRIC
from .asymmetric import WIDGETS_ASYMMETRIC
from .cryptotools import WIDGETS_CRYPTOTOOLS
from .cryptoprotocols import WIDGETS_CRYPTOPROTOCOLS
from .widgets import (
    BaseQThread,
    PBar
)

WIDGETS_CIPHERS = {
    "Symmetric ciphers": WIDGETS_SYMMETRIC,
    "Asymmetric ciphers": WIDGETS_ASYMMETRIC,
    "Cryptographic Protocols": WIDGETS_CRYPTOPROTOCOLS,
    "Crypto tools": WIDGETS_CRYPTOTOOLS
}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Crypto methods")

        # add fake spacer
        self.ui.status_bar.addWidget(QLabel(), 1)

        # add progress bar
        self.progress_bar = PBar()
        self.ui.status_bar.addWidget(self.progress_bar)
        self.progress_bar.close()

        # add button to reset the encryption/decryption process
        self.pbar_button_cancel = QPushButton()
        self.pbar_button_cancel.setText("×")
        self.ui.status_bar.addWidget(self.pbar_button_cancel)
        self.pbar_button_cancel.close()

        # show or hide the cancel button when showing or hiding the progress bar
        self.progress_bar.shown.connect(self.pbar_button_cancel.show)
        self.progress_bar.closed.connect(self.pbar_button_cancel.close)

        # file encryption workflow object
        self._thread_file_worker = None

        self.ui.splitter.setStretchFactor(1, 1)

        self.ui.tree_widget.clicked.connect(self.tree_widget_item_clicked)

        self._load_modules()
        self._check_dependencies()

    def _load_modules(self):
        # Load default modules
        for widget in WIDGETS_DEFAULT:
            self.ui.stacked_widget.addWidget(widget())

        # Load other widgets
        items = []

        for title, widgets in WIDGETS_CIPHERS.items():
            parent = QTreeWidgetItem((title,))
            parent.setIcon(0, QIcon("icons:folder.png"))

            children = []
            for widget in widgets:
                widget = widget()

                # we connect the signal of each widget to the method for
                # launching and setting the flow
                try:
                    widget.thread_ready.connect(self._task_start_handler)

                except AttributeError:
                    pass

                self.ui.stacked_widget.addWidget(widget)

                child = QTreeWidgetItem((widget.title,))
                child.setIcon(0, QIcon("icons:file.png"))
                child.setData(1, 1, widget)
                children.append(child)

            parent.addChildren(children)
            items.append(parent)

        self.ui.tree_widget.invisibleRootItem().addChildren(items)

    def tree_widget_item_clicked(self):
        item = self.ui.tree_widget.currentItem()
        widget = item.data(1, 1)

        match widget:
            case QWidget():
                self.ui.group_box_right.setTitle(item.text(0))
                self.ui.stacked_widget.setCurrentWidget(widget)

            case _:
                pass

    def _task_start_handler(self, thread: BaseQThread):
        if self._thread_file_worker is not None:
            if not self._thread_file_worker.isFinished():
                QMessageBox.warning(
                    self, "Warning!",
                    "You cannot start encrypting a new file until the old process is complete. "
                    "Cancel the current encryption process or try again later!")
                return

        self._thread_file_worker = thread
        # bind to receive and display error messages from the stream
        self._thread_file_worker.message.connect(lambda m: QMessageBox.warning(self, "Warning!", m))
        # bind to receive commands to initialize and update the progress bar
        self._thread_file_worker.pbar.connect(self.progress_bar.event_handler)
        # bind to stop the flow when the cancel button is clicked
        self.pbar_button_cancel.clicked.connect(self._thread_file_worker.close)
        self._thread_file_worker.start()

    def _check_dependencies(self):
        """Method for checking if required programs are installed or not."""
        programs = ("openssl",)

        for program in programs:
            if shutil.which(program) is None:
                QMessageBox.warning(self, "Warning!",
                                    f"{program} module not installed or not added to PATH")
