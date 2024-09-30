from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QRadioButton,
)

from viewmodels.vpn_indicator_view_model import (
    VPNIndicatorViewModel,
)
from .vpn_indicator import VPNIndicator
from .ping_view import PingView
from calabiyau_server_node_switcher.viewmodels.server_view_model import ServerViewModel


class ServerView(QWidget):
    def __init__(
        self,
        domain,
        ip,
        button_group,
        view_model: ServerViewModel,
    ):
        super().__init__()
        self.domain = domain
        self.ip = ip
        self.button_group = button_group
        self._view_model = view_model
        self.initUI()

    def __str__(self) -> str:
        return self.ip

    def __repr__(self) -> str:
        return self.ip

    def initUI(self):
        self.my_layout = QHBoxLayout()

        # IP Label
        self.ip_label = QLineEdit(self.ip)
        self.ip_label.setReadOnly(True)
        self.ip_label.setFixedWidth(110)
        self.my_layout.addWidget(self.ip_label)

        # Ping View
        self.my_layout.addWidget(PingView(self.ip))

        # Server selection button
        self.select_server_button = QRadioButton()
        self.button_group.addButton(self.select_server_button)
        self.select_server_button.setChecked(
            self._view_model.check_selected(),
        )
        self.select_server_button.toggled.connect(self.on_server_selected)
        self.my_layout.addWidget(self.select_server_button)

        # VPN indicator
        self.vpn_indicator_view_model = VPNIndicatorViewModel(self.ip)
        self.vpn_indicator = VPNIndicator(self.vpn_indicator_view_model)
        self.my_layout.addWidget(self.vpn_indicator)

        self.setLayout(self.my_layout)

    def on_server_selected(self):
        if self.select_server_button.isChecked():
            self._view_model.on_server_selected()
