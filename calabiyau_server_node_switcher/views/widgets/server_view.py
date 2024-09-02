from threading import Lock
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
)
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from models.get_route_table import get_network_destination_ips
from .ping_view import PingView
from models.routing_model import RoutingModel
from viewmodels.server_view_model import ServerViewModel


class ServerView(QWidget):
    def __init__(
        self,
        domain,
        ip,
        button_group,
    ):
        super().__init__()
        self.domain = domain
        self.ip = ip
        self.button_group = button_group
        self._view_model = ServerViewModel(self.domain, self.ip)
        RouteManager().route_signal.connect(self.on_route_changed)
        # RouteManager()
        self.initUI()

    def __str__(self) -> str:
        return self.ip

    def __repr__(self) -> str:
        return self.ip

    def initUI(self):
        self.my_layout = QHBoxLayout()

        # IP Label
        self.ip_label = QLineEdit(self.ip)
        self.ip_label.setReadOnly(True)
        self.ip_label.setFixedWidth(110)
        self.my_layout.addWidget(self.ip_label)

        # Ping View
        self.my_layout.addWidget(PingView(self.ip))

        # Server selection button
        self.select_server_button = QRadioButton()
        self.button_group.addButton(self.select_server_button)
        self.select_server_button.setChecked(
            self._view_model.check_selected(),
        )
        self.select_server_button.toggled.connect(self.on_server_selected)
        self.my_layout.addWidget(self.select_server_button)

        # VPN indicator
        self.vpn_label = QLabel("VPN: X")
        self.my_layout.addWidget(self.vpn_label)

        self.setLayout(self.my_layout)

    def on_server_selected(self):
        if self.select_server_button.isChecked():
            self._view_model.on_server_selected()

    def on_route_changed(self, data: list[RoutingModel]):
        for route in data:
            if route.is_route(self.ip):
                self.vpn_label.setText("VPN: O")
                break
            else:
                self.vpn_label.setText("VPN: X")


class Singleton(type(QObject), type):
    _lock = Lock()

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class RouteManager(QObject, metaclass=Singleton):
    route_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.list = []
            self.route_worker = RouteWorker()
            self.route_worker.route_worker_data.connect(self.on_route_changed)
            self.route_worker.start()

    def on_route_changed(self, data):
        self.list = data
        self.route_signal.emit(self.list)

    def stop_worker(self):
        if self.route_worker.isRunning():
            self.route_worker.stop()


class RouteWorker(QThread):
    route_worker_data = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        while self._running:
            self.route_worker_data.emit(get_network_destination_ips())
            self.sleep(2)

    def stop(self):
        self._running = False
        self.quit()
        self.wait()
