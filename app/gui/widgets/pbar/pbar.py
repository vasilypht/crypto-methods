from enum import Enum, auto

from PyQt6.QtWidgets import (
    QProgressBar
)
from PyQt6.QtCore import (
    pyqtSignal
)


class PBarCommands(Enum):
    SET_VALUE = auto()
    UPDATE_VALUE = auto()
    SET_RANGE = auto()
    SET_MIN_VALUE = auto()
    SET_MAX_VALUE = auto()
    CLOSE = auto()
    SHOW = auto()


class PBar(QProgressBar):
    shown = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(PBar, self).__init__(*args, **kwargs)

    def event_handler(self, option: tuple):
        match option:
            case PBarCommands.SET_VALUE, value:
                self.setValue(value)

            case PBarCommands.UPDATE_VALUE, value:
                current_value = self.value()
                self.setValue(current_value + value)

            case PBarCommands.SET_RANGE, min_value, max_value:
                self.setRange(min_value, max_value)

            case PBarCommands.SET_MIN_VALUE, min_value:
                self.setMinimum(min_value)

            case PBarCommands.SET_MAX_VALUE, max_value:
                self.setMaximum(max_value)

            case PBarCommands.CLOSE, *args:
                self.closed.emit()
                self.close()

            case PBarCommands.SHOW, *args:
                self.shown.emit()
                self.show()
