import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
)
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from change_hosts import ChangeHosts
from dns_servers import dns_servers
from domains import domains
import get_dns
from python_hosts import Hosts, HostsEntry
from ping_widget import PingWidget


class PingMainWidget(QWidget):
    def __init__(
        self,
        domain,
        ip_address,
        button_group,
        checked,
    ):
        super().__init__()
        self.domain = domain
        self.ip_address = ip_address
        self.button_group: QButtonGroup = button_group
        self.checked: bool = checked
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        # ip_address_label
        self.ip_address_label = QLineEdit(f"{self.ip_address}")
        self.ip_address_label.setReadOnly(True)
        self.layout.addWidget(self.ip_address_label)

        # ping_widget
        self.ping_widget = PingWidget(self.ip_address)
        self.layout.addWidget(self.ping_widget)

        # ping_color_indicator
        self.ping_color_indicator = QLabel()
        self.ping_color_indicator.setFixedSize(20, 20)
        self.layout.addWidget(self.ping_color_indicator)

        # ip_address_radio
        self.ip_address_radio = QRadioButton()
        self.ip_address_radio.setChecked(self.checked)
        self.ip_address_radio.toggled.connect(self.on_radio_button_toggled)
        self.button_group.addButton(self.ip_address_radio)
        self.layout.addWidget(self.ip_address_radio)

        self.setLayout(self.layout)

    @pyqtSlot()
    def on_radio_button_toggled(self):
        if self.ip_address_radio.isChecked():
            ChangeHosts(self.domain, self.ip_address).change()


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


class DomainWidget(QWidget):
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.domain_label = QLineEdit(f"Domain: {self.domain}")
        self.domain_label.setReadOnly(True)  # 편집 불가능하게 설정
        self.layout.addWidget(self.domain_label)

        self.button_group = QButtonGroup(self)

        self.setLayout(self.layout)

        self.get_ips_thread = GetIPsThread(self.domain)
        self.get_ips_thread.ips_fetched.connect(self.add_ping_widgets)
        self.get_ips_thread.start()

    def add_ping_widgets(self, ip_addresses):
        for ip_address in ip_addresses:
            ping_widget = PingMainWidget(
                self.domain,
                ip_address,
                self.button_group,
                self.add_checked_widgets(ip_address),
            )
            self.layout.addWidget(ping_widget)

    def add_checked_widgets(self, ip_address):
        hosts = Hosts()
        hostnames = []
        for entry in hosts.entries:
            if isinstance(entry, HostsEntry) and entry.names:
                hostnames.append(entry.address)
        if ip_address in hostnames:
            return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_widget = QWidget()
    main_layout = QHBoxLayout()  # 수평으로 배치

    for domain in domains:
        domain_widget = DomainWidget(domain)
        main_layout.addWidget(domain_widget)

    main_widget.setLayout(main_layout)
    main_widget.setWindowTitle("Calabiyau(卡拉彼丘) Server Changer - Please wait for a while")
    main_widget.setGeometry(100, 100, 1200, 600)
    main_widget.show()

    sys.exit(app.exec())
