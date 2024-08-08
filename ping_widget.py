from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from ping3 import ping
from time import sleep


class PingWidget(QWidget):
    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()

        self.ping_label = QLabel("Ping...")
        self.layout.addWidget(self.ping_label)

        self.ping_color_indicator = QLabel()
        self.ping_color_indicator.setFixedSize(20, 20)
        self.layout.addWidget(self.ping_color_indicator)

        self.setLayout(self.layout)

        self.ping_thread = PingThread(self.ip_address)
        self.ping_thread.ping_finished.connect(self.on_ping_finished)
        self.ping_thread.start()

    def on_ping_finished(self, ping):
        if ping == float("inf"):
            self.ping_label.setText("No response")
        else:
            self.ping_label.setText(f"{ping*1000:.2f} ms")
        self.update_ping_color_indicator(ping)

    def update_ping_color_indicator(self, ping):
        if ping < 0.05:
            color = "#45EF5D"  # Green
        elif ping < 0.1:
            color = "#FFD041"  # Yellow
        else:
            color = "#EB4353"  # Red
        self.ping_color_indicator.setStyleSheet(f"background-color: {color};")


class PingThread(QThread):
    ping_finished = pyqtSignal(float)

    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address

    def run(self):
        while True:
            sleep(0.5)  # delay 0.5 seconds
            response = None
            try:
                response = ping(self.ip_address)
                if response is None:
                    response = float("inf")
            except Exception as e:
                print(e)
                response = float("inf")
            self.ping_finished.emit(response)
