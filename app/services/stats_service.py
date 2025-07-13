"""
Statistics service for latency data
"""

from timeseries_db import get_latency_stats as _get_latency_stats


def get_latency_stats(region: str, server_addr: str, window: int):
    """
    Get latency statistics for a specific region and server

    Args:
        region: Server region
        server_addr: Server address
        window: Time window in seconds

    Returns:
        Latency statistics
    """
    return _get_latency_stats(region, server_addr, window)
