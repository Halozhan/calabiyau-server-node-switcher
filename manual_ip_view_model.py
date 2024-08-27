from PyQt6.QtCore import QObject, pyqtSignal

from change_hosts import ChangeHosts


class ManualIPViewModel(QObject):
    server_list_changed = pyqtSignal()

    def __init__(self, domain: str):
        super().__init__()
        self.domain = domain
        self.server_list = []
        self.server_list_view = dict()

    def on_reset_button_clicked(self):
        # reset_button을 클릭하면 hosts 파일을 초기화
        ChangeHosts(self.domain, "").remove()

    def add_server(self, server: str):
        if server not in self.server_list:
            # 서버가 중복되지 않도록 추가
            self.server_list.append(server)
            # 서버 리스트를 정렬
            self.server_list = sorted(self.server_list)
            # 서버 리스트가 변경되었음을 알림
            self.server_list_changed.emit()
