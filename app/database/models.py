"""
Database models and operations
"""

import sqlite3
import time
from typing import List, Dict, Optional, Tuple
from app.config import settings
from app.logging_config import get_logger

logger = get_logger("database")


async def init_db(db_path: Optional[str] = None) -> None:
    """Initialize database with required tables"""
    if db_path is None:
        db_path = settings.DATABASE_PATH

    try:
        logger.info(f"Initializing database: {db_path}")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS latency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER,
                region TEXT,
                domain TEXT,
                server_addr TEXT,
                port INTEGER,
                latency REAL
            )
            """
        )
        conn.commit()
        conn.close()

        # 데이터베이스 최적화 적용
        from app.database.optimizer import optimize_database

        optimize_database(db_path)

        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def insert_latency_record(
    region: str,
    domain: str,
    server_addr: str,
    port: int,
    latency: float,
    db_path: Optional[str] = None,
) -> None:
    """Insert latency record into database using batch writer"""
    try:
        # 배치 라이터 import (지연 import로 순환 참조 방지)
        from app.database.batch_writer import get_batch_writer

        batch_writer = get_batch_writer()
        success = batch_writer.add_record(region, domain, server_addr, port, latency)

        if not success:
            # 배치 라이터 실패 시 직접 DB에 쓰기 (fallback)
            logger.warning("Batch writer failed, using direct database write")
            _insert_latency_record_direct(
                region, domain, server_addr, port, latency, db_path
            )

    except Exception as e:
        logger.error(f"Failed to insert via batch writer: {e}")
        # fallback to direct insert
        _insert_latency_record_direct(
            region, domain, server_addr, port, latency, db_path
        )


def _insert_latency_record_direct(
    region: str,
    domain: str,
    server_addr: str,
    port: int,
    latency: float,
    db_path: Optional[str] = None,
) -> None:
    """Direct database insert (fallback method)"""
    if db_path is None:
        db_path = settings.DATABASE_PATH

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO latency (region, domain, server_addr, port, latency, "
        "timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (region, domain, server_addr, port, latency, int(time.time())),
    )
    conn.commit()
    conn.close()


def get_all_servers(db_path: Optional[str] = None) -> List[Dict[str, str]]:
    """Get all unique region, server_addr pairs from database"""
    if db_path is None:
        db_path = settings.DATABASE_PATH

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT DISTINCT region, server_addr FROM latency")
    rows = c.fetchall()
    conn.close()
    return [{"region": row[0], "server_addr": row[1]} for row in rows]


def get_latency_records(
    region: Optional[str] = None,
    server_addr: Optional[str] = None,
    limit: Optional[int] = None,
    db_path: Optional[str] = None,
) -> List[Tuple]:
    """Get latency records from database with optional filters"""
    if db_path is None:
        db_path = settings.DATABASE_PATH

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = "SELECT * FROM latency"
    params = []
    conditions = []

    if region:
        conditions.append("region = ?")
        params.append(region)

    if server_addr:
        conditions.append("server_addr = ?")
        params.append(server_addr)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY timestamp DESC"

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows
