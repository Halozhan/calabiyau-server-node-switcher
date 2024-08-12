import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
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


class ServerWidget(QWidget):
    def __init__(
        self,
        domain,
        ip_address,
        button_group,
    ):
        super().__init__()
        self.domain = domain
        self.ip_address = ip_address
        self.button_group: QButtonGroup = button_group
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

        # ip_address_radio
        self.ip_address_radio = QRadioButton()
        # 초기에 체크 상태를 설정
        self.ip_address_radio.setChecked(self.is_matched_ip_address())
        self.ip_address_radio.toggled.connect(self.on_radio_button_toggled)
        self.button_group.addButton(self.ip_address_radio)
        self.layout.addWidget(self.ip_address_radio)

        self.setLayout(self.layout)

    def is_matched_ip_address(self) -> bool:
        # hosts 파일을 읽어서 현재 ip_address가 있는지 확인
        hosts = Hosts()
        hostnames = []
        for entry in hosts.entries:
            if isinstance(entry, HostsEntry) and entry.names:
                hostnames.append(entry.address)
        if self.ip_address in hostnames:
            return True
        return False

    @pyqtSlot()
    def on_radio_button_toggled(self):
        if self.ip_address_radio.isChecked():
            ChangeHosts(self.domain, self.ip_address).change()


class GetIPThread(QThread):
    """
    dns_server로부터 domain에 대한 ip 주소를 가져오는 스레드
    """

    ip_fetched = pyqtSignal(str)

    def __init__(self, domain, dns_server):
        super().__init__()
        self.domain = domain
        self.dns_server = dns_server

    def run(self):
        ip_addresses = get_dns.query_domain(self.domain, [self.dns_server])
        # 여러 ip를 하나씩 보냄
        for ip_address in ip_addresses:
            self.ip_fetched.emit(ip_address)


class GetIPsThread(QThread):
    ips_fetched = pyqtSignal(list)

    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.ip_set = set()

    def run(self):
        get_ip_thread_list = []
        for dns_server in dns_servers:
            get_ip_thread = GetIPThread(self.domain, dns_server)
            get_ip_thread.ip_fetched.connect(self.on_ip_fetched)
            get_ip_thread.start()
            get_ip_thread_list.append(get_ip_thread)

        for get_ip_thread in get_ip_thread_list:
            get_ip_thread.wait()

    def on_ip_fetched(self, ip_address):
        """
        중복을 방지하여 ip 주소를 가져옴
        """
        if ip_address not in self.ip_set:
            self.ip_set.add(ip_address)
            ip_list = sorted(self.ip_set)
            self.ips_fetched.emit(ip_list)


class DomainWidget(QWidget):
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.ip_addresses_set = set()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # domain_label
        self.domain_layout = QHBoxLayout()
        self.domain_label = QLabel("Domain:")
        self.domain_layout.addWidget(self.domain_label)
        self.domain_name_label = QLineEdit(self.domain)
        self.domain_name_label.setReadOnly(True)
        self.domain_layout.addWidget(self.domain_name_label)
        self.layout.addLayout(self.domain_layout)

        # reset_button
        self.reset_button = QPushButton("set to default")
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.layout.addWidget(self.reset_button)

        self.button_group = QButtonGroup(self)

        self.ip_address_list_box_layout = QVBoxLayout()
        self.layout.addLayout(self.ip_address_list_box_layout)

        self.setLayout(self.layout)

        self.get_ips_thread = GetIPsThread(self.domain)
        self.get_ips_thread.ips_fetched.connect(self.on_ips_fetched)
        self.get_ips_thread.start()

    def on_reset_button_clicked(self):
        # reset_button을 클릭하면 hosts 파일을 초기화
        ChangeHosts(self.domain, "").remove()
        self.render_ping_widgets()  # ping_widget을 다시 렌더링

    def on_ips_fetched(self, ip_addresses):
        # ip 주소를 가져오면 ping_widget을 렌더링
        self.ip_addresses_list = ip_addresses
        self.render_ping_widgets()

    def render_ping_widgets(self):
        # 기존의 ping_widget을 모두 제거
        self.clear_layout(self.ip_address_list_box_layout)

        # 새로운 ping_widget을 추가
        for ip_address in self.ip_addresses_list:
            ping_widget = ServerWidget(
                self.domain,
                ip_address,
                self.button_group,
            )
            self.ip_address_list_box_layout.addWidget(ping_widget)

    def clear_layout(self, layout):
        # 레이아웃에 있는 모든 위젯을 제거
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout.removeItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_widget = QWidget()
    main_layout = QHBoxLayout()  # 수평으로 배치

    for domain in domains:
        domain_widget = DomainWidget(domain)
        main_layout.addWidget(domain_widget)

    main_widget.setLayout(main_layout)
    main_widget.setWindowTitle(
        "Calabiyau(卡拉彼丘) Server Changer - Please restart your game after changing the server"
    )
    main_widget.setGeometry(100, 100, 1200, 600)
    main_widget.show()

    sys.exit(app.exec())
