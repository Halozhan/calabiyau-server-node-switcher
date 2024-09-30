from PyQt6.QtCore import QObject, pyqtSignal, QThread

from models.get_route_table import get_network_destination_ips
from .singleton import Singleton


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
