from PyQt6.QtWidgets import (
    QWidget
)
from PyQt6.QtCore import (
    pyqtSignal
)
from ..base_qthread.base_qthread import BaseQThread


class BaseQWidget(QWidget):
    thread_ready = pyqtSignal(BaseQThread)

    def __init__(self, *args, **kwargs):
        super(BaseQWidget, self).__init__(*args, **kwargs)

        self.title = "None"
