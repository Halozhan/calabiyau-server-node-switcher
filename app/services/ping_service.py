"""
Ping service for latency testing
"""

import asyncio
from typing import Optional
from app.network.latency_measurement import measure_latency
from app.database.models import insert_latency_record
from app.logging_config import get_logger

logger = get_logger("ping_service")


async def ping_worker(region: str, domain: str, ip: str, port: int) -> None:
    """
    Ping a single server and record the result

    Args:
        region: Server region
        domain: Server domain
        ip: Server IP address
        port: Server port
    """
    result = await measure_latency(ip, port=port)

    if "latency" in result:
        # 성공
        latency = float(result["latency"])
        print(f"{domain} - {ip}:{port}: {latency:.2f} ms (성공)")
        logger.info(f"{domain} - {ip}:{port}: {latency:.2f} ms (성공)")
    else:
        # 실패
        latency = -1.0
        print(f"{domain} - {ip}:{port}: 실패: {result}")
        logger.error(f"{domain} - {ip}:{port}: 실패: {result}")

    # 결과를 DB에 저장
    insert_latency_record(region, domain, ip, port, latency)


async def ping_all_servers(
    server_list: dict, port_override: Optional[int] = None
) -> None:
    """
    Ping all servers in the server list

    Args:
        server_list: Dictionary containing server information
        port_override: Optional port override
    """
    tasks = []

    for region, info in server_list.items():
        port = port_override or info.get("port", 20000)
        for node in info.get("nodes", []):
            for domain, ips in node.items():
                for ip in ips:
                    tasks.append(
                        asyncio.create_task(ping_worker(region, domain, ip, port))
                    )

    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
