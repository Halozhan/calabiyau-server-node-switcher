from PyQt6.QtCore import QObject
from python_hosts import Hosts, HostsEntry

from change_hosts import ChangeHosts


class ServerViewModel(QObject):

    def __init__(self, domain: str, ip: str):
        super().__init__()
        self.domain = domain
        self.ip = ip

    def check_selected(self) -> bool:
        # 서버가 선택되었는지 확인
        hosts = Hosts()
        hostnames = []
        for entry in hosts.entries:
            if isinstance(entry, HostsEntry) and entry.names:
                hostnames.append(entry.address)
        if self.ip in hostnames:
            return True

        return False

    def on_server_selected(self):
        # 서버 선택 시 hosts 파일에 추가
        ChangeHosts(self.domain, self.ip).change()
