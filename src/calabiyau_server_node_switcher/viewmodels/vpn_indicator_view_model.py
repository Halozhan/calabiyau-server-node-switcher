from PyQt6.QtCore import QObject, pyqtSignal

from models.routing_model import RoutingModel
from utils.route_manager import RouteManager


class VPNIndicatorViewModel(QObject):
    vpn_status_changed = pyqtSignal(str)

    def __init__(self, ip: str):
        super().__init__()
        self.ip = ip
        self.vpn_status = "?"
        RouteManager().route_signal.connect(self.on_route_changed)

    def on_route_changed(self, data: list[RoutingModel]):
        for route in data:
            if route.is_route(self.ip):
                self.vpn_status_changed.emit("O")
                break
            else:
                self.vpn_status_changed.emit("X")
