"""
Network module for DNS queries and latency measurements
"""

from .dns_resolver import query_server, query_all_servers, discover_servers_from_config
from .latency_measurement import (
    measure_latency,
    measure_multiple_latencies,
    query_ping,  # 하위 호환성을 위한 별칭
)

__all__ = [
    "query_server",
    "query_all_servers",
    "discover_servers_from_config",
    "measure_latency",
    "measure_multiple_latencies",
    "query_ping",
]
