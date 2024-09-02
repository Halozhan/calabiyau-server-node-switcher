from viewmodels.manual_ip_view_model import ManualIPViewModel
from .server_view import ServerView

from PyQt6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLayout,
)


class ManualIPView(QWidget):
    def __init__(self, domain: str, server_list: list):
        super().__init__()
        self.domain = domain
        self._view_model = ManualIPViewModel(self.domain)
        self._view_model.server_list = server_list
        self._view_model.server_list_changed.connect(
            self.on_server_list_changed,
        )
        self.server_list = []
        self.initUI()
        self.render_server_list()

    def initUI(self):
        self.my_layout = QVBoxLayout(self)

        # Domain Layout
        self.domain_layout = QHBoxLayout()
        self.domain_label = QLabel("Domain:")
        self.domain_layout.addWidget(self.domain_label)
        self.domain_name_label = QLineEdit(self.domain)
        self.domain_name_label.setReadOnly(True)
        self.domain_layout.addWidget(self.domain_name_label)
        self.my_layout.addLayout(self.domain_layout)

        # Reset button
        self.reset_button = QPushButton("set to default")
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.my_layout.addWidget(self.reset_button)

        # Server Layout
        self.server_list_layout = QVBoxLayout()
        self.select_server_group = QButtonGroup()
        self.my_layout.addLayout(self.server_list_layout)

    def on_reset_button_clicked(self):
        self._view_model.on_reset_button_clicked()
        # 리셋 버튼을 누르면 다시 서버 리스트를 렌더링한다.
        self.on_server_list_changed()

    def on_server_list_changed(self):
        # 서버 리스트가 변경되면 레이아웃을 지운다.
        self.clear_layout(self.server_list_layout)
        # 서버 리스트를 다시 렌더링한다.
        self.render_server_list()

    def clear_layout(self, layout: QLayout):
        # 레이아웃에 있는 모든 위젯을 제거
        while layout.count():
            item = layout.takeAt(0)
            if item is not None:
                widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                # 만약 레이아웃이 중첩되어 있는 경우, 해당 레이아웃에 대해서도 삭제를 진행합니다.
                if item is not None:
                    sub_layout = item.layout()
                if sub_layout is not None:
                    print("sub_layout")
                    self.clear_layout(sub_layout)

    def render_server_list(self):
        for ip in self._view_model.server_list:
            if ip not in self.server_list:
                server = ServerView(self.domain, ip, self.select_server_group)
                self.server_list.append(server)
                self.server_list_layout.addWidget(server)
