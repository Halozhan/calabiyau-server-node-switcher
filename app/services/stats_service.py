"""
Statistics service for latency data
"""

import sqlite3
import time
from typing import Dict
from app.config import settings
from app.logging_config import get_logger

logger = get_logger("stats_service")


def get_latency_stats(region: str, server_addr: str, window: int) -> Dict:
    """
    Get latency statistics for a specific region and server

    Args:
        region: Server region
        server_addr: Server address
        window: Time window in seconds

    Returns:
        Latency statistics with avg, min, max, loss_rate, count, raw_data
    """
    try:
        now = int(time.time())
        conn = sqlite3.connect(settings.DATABASE_PATH)
        c = conn.cursor()

        # 지정된 시간 윈도우 내의 레이턴시 데이터 조회
        c.execute(
            """
            SELECT latency FROM latency
            WHERE region = ? AND server_addr = ? AND timestamp >= ?
            ORDER BY timestamp DESC
            """,
            (region, server_addr, now - window),
        )
        rows = c.fetchall()

        # raw_data를 위한 timestamp 포함 조회
        c.execute(
            """
            SELECT timestamp, latency FROM latency
            WHERE region = ? AND server_addr = ? AND timestamp >= ?
            ORDER BY timestamp ASC
            """,
            (region, server_addr, now - window),
        )
        raw_rows = c.fetchall()
        conn.close()

        # 레이턴시가 0보다 큰 것만 성공으로 간주
        all_latencies = [row[0] for row in rows]
        successful_latencies = [lat for lat in all_latencies if lat > 0]

        count = len(all_latencies)
        success_count = len(successful_latencies)
        loss_count = count - success_count
        loss_rate = loss_count / count if count > 0 else 0

        if successful_latencies:
            avg = sum(successful_latencies) / len(successful_latencies)
            min_latency = min(successful_latencies)
            max_latency = max(successful_latencies)
        else:
            avg = 0
            min_latency = 0
            max_latency = 0

        # raw_data 생성
        raw_data = [{"timestamp": row[0], "latency": row[1]} for row in raw_rows]

        return {
            "avg": avg,
            "min": min_latency,
            "max": max_latency,
            "loss_rate": loss_rate,
            "count": count,
            "raw_data": raw_data,
        }

    except Exception as e:
        logger.error(f"Failed to get latency stats: {e}")
        return {
            "avg": 0,
            "min": 0,
            "max": 0,
            "loss_rate": 1.0,
            "count": 0,
            "raw_data": [],
        }
