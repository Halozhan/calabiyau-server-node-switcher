from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
)

from domain_view import DomainView
from domains import domains


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(
            "Calabiyau(卡拉彼丘) Server Node Changer - \
Please restart your game after changing the server"
        )

        # Set the central widget of the Window.
        # Widget will expand to take up all the space in the window by default
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout and set it on the central widget
        self.my_layout = QHBoxLayout(central_widget)

        # Domain view
        for domain in domains:
            self.domain_view = DomainView(domain)
            self.my_layout.addWidget(self.domain_view)
