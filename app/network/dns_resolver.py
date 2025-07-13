"""
DNS query module for server discovery
"""

import json
import dns.asyncresolver
import dns.resolver
import asyncio
from typing import List, Optional, Dict, Any
from app.logging_config import get_logger

logger = get_logger("dns_query")


async def query_server(domain: str) -> Optional[List[str]]:
    """
    Query DNS A records for a domain

    Args:
        domain: Domain name to query

    Returns:
        List of IP addresses or None if query fails
    """
    resolver = dns.asyncresolver.Resolver()
    server = []
    try:
        answer = await resolver.resolve(domain, "A")
        if not answer:
            return None
        for record in answer:
            ip = str(record)  # Convert to string
            server.append(ip)
        return server
    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.LifetimeTimeout,
    ) as e:
        logger.warning(f"DNS query failed for {domain}: {e}")
        raise e


async def query_all_servers(
    server_list: Dict[str, Any], max_servers: int = 150
) -> List[Dict[str, Any]]:
    """
    Query all servers from server list

    Args:
        server_list: Dictionary containing server configurations
        max_servers: Maximum number of servers to query per region

    Returns:
        List of server information with resolved IPs
    """
    tasks = []

    for region, info in server_list.items():
        for i in range(1, max_servers + 1):
            domain = info["domain"].replace("{iterable}", str(i))
            task_info = {
                "region": region,
                "domain": domain,
                "port": info["port"],
                "index": i,
            }
            tasks.append((query_server(domain), task_info))

    results = []
    try:
        # Execute DNS queries
        dns_tasks = [task[0] for task in tasks]
        dns_results = await asyncio.gather(*dns_tasks, return_exceptions=True)

        # Process results
        for result, (_, info) in zip(dns_results, tasks):
            if isinstance(result, list) and result:  # Successful query
                for ip in result:
                    results.append(
                        {
                            "region": info["region"],
                            "domain": info["domain"],
                            "server_addr": ip,
                            "port": info["port"],
                            "index": info["index"],
                        }
                    )
            elif isinstance(result, Exception):
                logger.debug(f"Failed to resolve {info['domain']}: {result}")

    except Exception as e:
        logger.error(f"Error in query_all_servers: {e}")

    logger.info(f"Discovered {len(results)} servers from DNS queries")
    return results


async def discover_servers_from_config(config_path: str) -> List[Dict[str, Any]]:
    """
    Discover servers from configuration file

    Args:
        config_path: Path to server list JSON file

    Returns:
        List of discovered servers
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            server_list = json.load(f)

        return await query_all_servers(server_list)

    except Exception as e:
        logger.error(f"Failed to discover servers from {config_path}: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    async def main():
        server_list = {"테스트": {"domain": "example{iterable}.com", "port": 80}}
        results = await query_all_servers(server_list, max_servers=3)
        print(f"Found {len(results)} servers")
        for server in results:
            print(f"{server['region']}: {server['server_addr']}")

    asyncio.run(main())
