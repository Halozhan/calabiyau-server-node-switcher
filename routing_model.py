from threading import Lock
from typing import List, Optional


class RoutingModel:
    def __init__(self, ip: str, subnet_mask: str, gateway: str):
        self.ip = ip
        self.subnet_mask = subnet_mask
        self.gateway = gateway

    def __str__(self):
        return f"{self.ip} {self.subnet_mask} {self.gateway}"

    def is_route(self, comparison_ip: str) -> bool:
        if self.subnet_mask == "255.255.255.255" and self.ip == comparison_ip:
            return True
        elif (
            self.subnet_mask == "255.255.255.0"
            and self.ip.split(".")[0:3] == comparison_ip.split(".")[0:3]
        ):
            return True
        elif (
            self.subnet_mask == "255.255.0.0"
            and self.ip.split(".")[0:2] == comparison_ip.split(".")[0:2]
        ):
            return True
        elif (
            self.subnet_mask == "255.0.0.0"
            and self.ip.split(".")[0] == comparison_ip.split(".")[0]
        ):
            return True
        else:
            return False


class RoutingModelList(type):

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.routing_models: List[RoutingModel] = []

    def get_route(self, comparison_ip: str) -> Optional[RoutingModel]:
        for routing_model in self.routing_models:
            if routing_model.is_route(comparison_ip):
                return routing_model

        return None
