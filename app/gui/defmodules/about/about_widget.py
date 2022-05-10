import webbrowser

from PyQt6.QtWidgets import (
    QWidget
)
from PyQt6.QtGui import (
    QIcon
)

from .about_ui import Ui_about


class AboutWidget(QWidget):
    def __init__(self):
        super(AboutWidget, self).__init__()
        self.ui = Ui_about()
        self.ui.setupUi(self)

        self.title = "About"

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
