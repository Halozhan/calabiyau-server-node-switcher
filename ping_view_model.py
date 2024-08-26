from time import sleep
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from ping3 import ping


class PingViewModel(QObject):
    ping_response = pyqtSignal(float)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.get_ping()

    def get_ping(self):
        self.ping_thread = PingWorker(self.ip)
        self.ping_thread.ping_response.connect(self.emit_ping)
        self.ping_thread.start()

    def emit_ping(self, ping_response):
        self.ping_response.emit(ping_response)


class PingWorker(QThread):
    ping_response = pyqtSignal(float)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self._running = True

    def run(self):
        while self._running:
            sleep(0.5)
            response = None
            try:
                response = ping(self.ip)
                if response is None:
                    response = float("inf")
            except Exception as e:
                print(e)
                response = float("inf")
            self.ping_response.emit(response)

    def stop(self):
        self._running = False
        self.quit()
        self.wait()
