"""
API routes and endpoints
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from app.services.stats_service import get_latency_stats
from app.database.models import get_all_servers
from app.config import config
from app.logging_config import get_logger

router = APIRouter()
logger = get_logger("api")


@router.get("/config")
def get_config():
    """
    클라이언트가 interval_ms를 요청할 때 사용
    """
    try:
        logger.info("Configuration requested")
        return {"interval_ms": config["interval_ms"]}
    except Exception as e:
        logger.error(f"Failed to get configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to get configuration")


@router.post("/config")
def set_config(interval_ms: Optional[int] = Query(None)):
    """
    클라이언트가 interval_ms를 설정할 때 사용
    """
    try:
        if interval_ms is not None:
            if interval_ms < 10:
                logger.warning(f"Invalid interval_ms: {interval_ms} (too small)")
                raise HTTPException(
                    status_code=400, detail="interval_ms must be at least 10ms"
                )
            config["interval_ms"] = interval_ms
            logger.info(f"Configuration updated: interval_ms={interval_ms}")

        return {"interval_ms": config["interval_ms"]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to set configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to set configuration")


@router.get("/stats")
def stats(
    region: str = Query(...), server_addr: str = Query(...), window: int = Query(30)
):
    """
    region, server_addr, window(초)로 최근 통계 반환
    """
    try:
        if window <= 0:
            logger.warning(f"Invalid window value: {window}")
            raise HTTPException(status_code=400, detail="Window must be positive")

        logger.info(f"Stats requested: {region}, {server_addr}, {window}s")
        result = get_latency_stats(region, server_addr, window)

        if not result:
            logger.warning(f"No stats found for {region}, {server_addr}")

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")


@router.get("/servers")
def get_servers() -> List[Dict[str, str]]:
    """
    DB에서 region, server_addr의 유니크 쌍을 모두 반환
    """
    try:
        logger.info("Server list requested")
        servers = get_all_servers()
        logger.info(f"Returning {len(servers)} servers")
        return servers
    except Exception as e:
        logger.error(f"Failed to get servers: {e}")
        raise HTTPException(status_code=500, detail="Failed to get server list")
