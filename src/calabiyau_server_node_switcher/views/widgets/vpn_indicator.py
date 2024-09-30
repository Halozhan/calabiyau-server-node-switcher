from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSlot

from viewmodels.vpn_indicator_view_model import VPNIndicatorViewModel


class VPNIndicator(QWidget):
    def __init__(self, view_model: VPNIndicatorViewModel):
        super().__init__()
        self._view_model = view_model
        self._view_model.vpn_status_changed.connect(self.on_vpn_status_changed)
        self.initUI()

    def initUI(self):
        self.my_layout = QHBoxLayout()

        self.vpn_label = QLabel("VPN: ?")
        self.my_layout.addWidget(self.vpn_label)

        self.setLayout(self.my_layout)

    @pyqtSlot(str)
    def on_vpn_status_changed(self, status):
        self.vpn_label.setText(f"VPN: {status}")
