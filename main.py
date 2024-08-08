import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from ping3 import ping
from dns_servers import dns_servers
from domains import domains
import get_dns


class PingThread(QThread):
    ping_finished = pyqtSignal(float)

    def __init__(self, address):
        super().__init__()
        self.address = address

    def run(self):
        try:
            response = ping(self.address, timeout=2)
            result = response if response is not None else float("inf")
        except Exception:
            result = float("inf")
        self.ping_finished.emit(result)


class PingWidget(QWidget):
    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLineEdit(f"Pinging {self.ip_address}...")
        self.label.setReadOnly(True)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ping)
        self.timer.start(500)  # Update every

    def update_ping(self):
        self.ping_thread = PingThread(self.ip_address)
        self.ping_thread.ping_finished.connect(self.update_ping_label)
        self.ping_thread.start()

    def update_ping_label(self, ping):
        self.label.setText(f"{self.ip_address}: {ping * 1000:.2f} ms")


class GetIPsThread(QThread):
    ips_fetched = pyqtSignal(list)

    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def run(self):
        self.ip_addresses = get_dns.get_ip_addresses_from_multiple_dns(
            self.domain, dns_servers
        )
        self.ips_fetched.emit(self.ip_addresses)


class DomainPingWidget(QWidget):
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.domain_label = QLineEdit(f"Domain: {self.domain}")
        self.domain_label.setReadOnly(True)  # 편집 불가능하게 설정
        self.layout.addWidget(self.domain_label)
        self.setLayout(self.layout)

        self.get_ips_thread = GetIPsThread(self.domain)
        self.get_ips_thread.ips_fetched.connect(self.add_ping_widgets)
        self.get_ips_thread.start()

    def add_ping_widgets(self, ip_addresses):
        for ip_address in ip_addresses:
            ping_widget = PingWidget(ip_address)
            self.layout.addWidget(ping_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_widget = QWidget()
    main_layout = QHBoxLayout()

    for domain in domains:
        domain_ping_widget = DomainPingWidget(domain)
        main_layout.addWidget(domain_ping_widget)

    main_widget.setLayout(main_layout)
    main_widget.setWindowTitle("Calabiyau Server Ping Monitor")
    main_widget.setGeometry(100, 100, 1000, 600)
    main_widget.show()

    sys.exit(app.exec())
