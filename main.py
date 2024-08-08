import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from ping3 import ping
import get_dns


class PingWidget(QWidget):
    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel(f"Pinging {self.ip_address}...")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ping)
        self.timer.start(500)  # Update every

    def update_ping(self):
        ping_result = self.get_ping(self.ip_address)
        self.label.setText(f"{self.ip_address}: {ping_result * 1000:.2f} ms")

    def get_ping(self, address):
        try:
            response = ping(address, timeout=2)
            return response if response is not None else float("inf")
        except Exception:
            return float("inf")


class GetIPsThread(QThread):
    ips_fetched = pyqtSignal(set)

    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def run(self):
        self.ip_addresses = get_dns.get_ip_addresses_from_multiple_dns(
            self.domain, get_dns.dns_servers
        )
        self.ips_fetched.emit(self.ip_addresses)


class DomainPingWidget(QWidget):
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.domain_label = QLabel(f"Domain: {self.domain}")
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

    domains = [
        "ds-tj-1.klbq.qq.com",
        "ds-nj-1.klbq.qq.com",
        "ds-gz-1.klbq.qq.com",
        "ds-cq-1.klbq.qq.com",
    ]
    for domain in domains:
        domain_ping_widget = DomainPingWidget(domain)
        main_layout.addWidget(domain_ping_widget)

    main_widget.setLayout(main_layout)
    main_widget.setWindowTitle("Calabiyau Server Ping Monitor")
    main_widget.setGeometry(100, 100, 1000, 600)
    main_widget.show()

    sys.exit(app.exec())
