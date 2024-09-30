from PyQt6.QtCore import QObject
from threading import Lock


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
