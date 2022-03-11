import webbrowser

from PyQt6.QtWidgets import (
    QWidget
)
from PyQt6.QtGui import (
    QIcon
)

from src.application.modules.info.info_ui import Ui_info


class InfoWidget(QWidget):
    def __init__(self):
        super(InfoWidget, self).__init__()
        self.ui = Ui_info()
        self.ui.setupUi(self)

        self.title = "Info"

        self.ui.button_vk.setIcon(QIcon("icons:vk.png"))
        self.ui.button_vk.clicked.connect(
            lambda: webbrowser.open(f"https://{self.ui.button_vk.text()}")
        )

        self.ui.button_tg.setIcon(QIcon("icons:telegram.png"))
        self.ui.button_tg.clicked.connect(
            lambda: webbrowser.open(f"https://{self.ui.button_tg.text()}")
        )

        self.ui.button_github.setIcon(QIcon("icons:github.png"))
        self.ui.button_github.clicked.connect(
            lambda: webbrowser.open(f"https://{self.ui.button_github.text()}")
        )
