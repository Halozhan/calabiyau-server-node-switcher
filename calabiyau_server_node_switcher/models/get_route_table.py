import subprocess
import re

from .routing_model import RoutingModel


def get_route_table():
    result = subprocess.run(
        ["route", "print", "-4"], capture_output=True, text=True, shell=True
    )
    return result


def extract_ips(ip_list):
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    routing_models = []

    for line in ip_list:
        parts = line.split()
        if len(parts) >= 3:
            ip = parts[0]
            subnet_mask = parts[1]
            gateway = parts[2]
            if (
                ip_pattern.match(ip)
                and ip_pattern.match(subnet_mask)
                and ip_pattern.match(gateway)
            ):
                routing_models.append(RoutingModel(ip, subnet_mask, gateway))

    return routing_models


def extract_network_destination_ips(data):
    """IP addresses are in the first column of the table"""
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    network_destination_ips = []

    for line in data:
        if (
            line.strip()
            and not line.startswith("Network Destination")
            and not line.startswith("Active Routes:")
        ):
            parts = line.split()
            if parts:
                ip = parts[0]
                if ip_pattern.match(ip):
                    network_destination_ips.append(ip)

    return network_destination_ips


def get_network_destination_ips():
    response = get_route_table()
    response_list = response.stdout.split("\n")

    ips: list[RoutingModel] = extract_ips(response_list)

    return ips


if __name__ == "__main__":

    response = get_route_table()
    response_list = response.stdout.split("\n")

    collect = False
    ip_list = []
    for i in response_list:
        if i == "Active Routes:":
            collect = True
        if collect:
            ip_list.append(i)
        if i == "Persistent Routes:":
            collect = False

    ips = extract_ips(ip_list)
    # print(ips)

    network_destination_ips = extract_network_destination_ips(ip_list)
    print(network_destination_ips)
