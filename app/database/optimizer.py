"""
데이터베이스 최적화 설정 및 유틸리티
"""

import sqlite3
from typing import Optional
from app.config import settings
from app.logging_config import get_logger

logger = get_logger("db_optimize")


def optimize_database(db_path: Optional[str] = None) -> None:
    """데이터베이스 성능 최적화 설정 적용"""
    if db_path is None:
        db_path = settings.DATABASE_PATH

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # WAL 모드 활성화 (Write-Ahead Logging)
        # 읽기와 쓰기가 동시에 가능하도록 함
        cursor.execute("PRAGMA journal_mode=WAL")

        # 동기화 모드를 NORMAL로 설정 (기본값 FULL보다 빠름)
        cursor.execute("PRAGMA synchronous=NORMAL")

        # 캐시 크기 증가 (기본값: 2000, 증가값: 10000)
        cursor.execute("PRAGMA cache_size=10000")

        # 메모리 매핑 크기 설정 (256MB)
        cursor.execute("PRAGMA mmap_size=268435456")

        # 임시 저장소를 메모리에 설정
        cursor.execute("PRAGMA temp_store=MEMORY")

        # 인덱스 생성 (자주 검색되는 컬럼들)
        try:
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_latency_region_server_time
                ON latency(region, server_addr, timestamp)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_latency_timestamp
                ON latency(timestamp)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_latency_region_server
                ON latency(region, server_addr)
            """
            )
        except Exception as e:
            logger.warning(f"Index creation failed (may already exist): {e}")

        conn.commit()
        conn.close()

        logger.info("Database optimization completed successfully")

    except Exception as e:
        logger.error(f"Failed to optimize database: {e}")
        raise


def cleanup_old_records(db_path: Optional[str] = None, days_to_keep: int = 7) -> int:
    """오래된 레코드 정리 (성능 향상을 위해)"""
    if db_path is None:
        db_path = settings.DATABASE_PATH

    try:
        import time

        cutoff_timestamp = int(time.time()) - (days_to_keep * 24 * 3600)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 오래된 레코드 삭제
        cursor.execute("DELETE FROM latency WHERE timestamp < ?", (cutoff_timestamp,))

        deleted_count = cursor.rowcount

        # VACUUM 실행 (디스크 공간 회수)
        cursor.execute("VACUUM")

        conn.commit()
        conn.close()

        logger.info(
            f"Cleaned up {deleted_count} old records (older than {days_to_keep} days)"
        )
        return deleted_count

    except Exception as e:
        logger.error(f"Failed to cleanup old records: {e}")
        return 0


def get_database_stats(db_path: Optional[str] = None) -> dict:
    """데이터베이스 통계 정보 반환"""
    if db_path is None:
        db_path = settings.DATABASE_PATH

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 전체 레코드 수
        cursor.execute("SELECT COUNT(*) FROM latency")
        total_records = cursor.fetchone()[0]

        # 고유 서버 수
        cursor.execute(
            "SELECT COUNT(DISTINCT region || '-' || server_addr) FROM latency"
        )
        unique_servers = cursor.fetchone()[0]

        # 최신 레코드 타임스탬프
        cursor.execute("SELECT MAX(timestamp) FROM latency")
        latest_timestamp = cursor.fetchone()[0]

        # 가장 오래된 레코드 타임스탬프
        cursor.execute("SELECT MIN(timestamp) FROM latency")
        oldest_timestamp = cursor.fetchone()[0]

        # 데이터베이스 파일 크기
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]
        db_size_bytes = page_size * page_count

        conn.close()

        return {
            "total_records": total_records,
            "unique_servers": unique_servers,
            "latest_timestamp": latest_timestamp,
            "oldest_timestamp": oldest_timestamp,
            "db_size_bytes": db_size_bytes,
            "db_size_mb": round(db_size_bytes / (1024 * 1024), 2),
        }

    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}
