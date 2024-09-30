from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSlot

from viewmodels.ping_view_model import PingViewModel


class PingView(QWidget):
    GREEN = "#45EF5D"
    YELLOW = "#FFD041"
    RED = "#EB4353"

    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self._view_model = PingViewModel(self.ip)
        self._view_model.ping_response.connect(self.on_ping_response)
        self.initUI()

    def initUI(self):
        self.my_layout = QHBoxLayout()

        # Ping Label
        self.ping_label = QLabel("Ping...")
        self.my_layout.addWidget(self.ping_label)

        # Ping Indicator
        self.ping_indicator = QLabel()
        self.ping_indicator.setFixedSize(20, 20)
        self.ping_indicator.setStyleSheet(f"background-color: {self.GREEN};")
        self.my_layout.addWidget(self.ping_indicator)

        self.setLayout(self.my_layout)

    @pyqtSlot(float)
    def on_ping_response(self, ping):
        self.set_ping_label(ping)
        self.set_ping_indicator(ping)

    def set_ping_label(self, ping):
        if ping == float("inf"):
            self.ping_label.setText("N/A")
        else:
            self.ping_label.setText(f"{ping*1000:.2f}ms")

    def set_ping_indicator(self, ping):
        if ping < 0.05:
            color = self.GREEN
        elif ping < 0.1:
            color = self.YELLOW
        else:
            color = self.RED
        self.ping_indicator.setStyleSheet(f"background-color: {color};")

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # Stop the ping thread
        self._view_model.ping_thread.quit()
        self._view_model.ping_thread.wait()
        return super().closeEvent(a0)
