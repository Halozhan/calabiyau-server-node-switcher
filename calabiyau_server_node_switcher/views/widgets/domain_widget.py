from viewmodels.domain_view_model import DomainViewModel
from viewmodels.server_view_model import ServerViewModel
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
from PyQt6.QtCore import pyqtSlot


class DomainWidget(QWidget):
    def __init__(self, domain: str, view_model: DomainViewModel):
        super().__init__()
        self.domain = domain
        self._view_model = view_model
        self._view_model.server_list_changed.connect(
            self.on_server_list_changed,
        )
        self.initUI()

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
        self.reset_button.clicked.connect(
            self._view_model.on_reset_button_clicked,
        )
        self.my_layout.addWidget(self.reset_button)

        # Server Layout
        self.server_list_layout = QVBoxLayout()
        self.select_server_group = QButtonGroup()
        self.my_layout.addLayout(self.server_list_layout)

    @pyqtSlot(list)
    def on_server_list_changed(self, server_list: list):
        # 서버 리스트가 변경되면 레이아웃을 지운다.
        self.clear_layout(self.server_list_layout)
        # 서버 리스트를 다시 렌더링한다.
        self.render_server_list(server_list)

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

    def render_server_list(self, server_list: list):
        for ip in server_list:
            self.server_view_model = ServerViewModel(self.domain, ip)
            self.server = ServerView(
                domain=self.domain,
                ip=ip,
                button_group=self.select_server_group,
                view_model=self.server_view_model,
            )
            self.server_list_layout.addWidget(self.server)
