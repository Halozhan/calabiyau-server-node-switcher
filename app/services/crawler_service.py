"""
Crawler service for DNS queries and server discovery
"""

import json
from typing import Dict
from dns_query.query_servers import query_server
from app.config import settings
from app.logging_config import get_logger

logger = get_logger("crawler_service")


async def load_server_list() -> Dict:
    """Load server list from JSON file"""
    with open(settings.SERVER_LIST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


async def discover_servers() -> Dict:
    """
    Discover all available servers by querying DNS

    Returns:
        Updated server list with discovered nodes
    """
    server_list = await load_server_list()

    # DNS 쿼리 수행
    for region, info in server_list.items():
        logger.info(f"쿼리 중: {region} - {info['domain']}")
        for i in range(1, settings.MAX_SERVERS_PER_REGION + 1):
            domain = info["domain"].replace("{iterable}", str(i))
            logger.info(f"쿼리 도메인: {domain}")
            try:
                # 쿼리 결과를 저장
                results = await query_server(domain)
                if "nodes" not in info:
                    info["nodes"] = []
                info["nodes"].append({domain: results})
                logger.info(f"쿼리 결과: {results}")
            except Exception as e:
                logger.error(f"쿼리 실패: {domain} - {e}")
                # 쿼리 실패 시 이후에 더 이상 서버가 없다고 가정하고 탈출
                break

    logger.info("모든 서버 쿼리 완료")
    return server_list
