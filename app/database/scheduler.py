"""
데이터베이스 관리 작업을 위한 스케줄러
"""

import asyncio
from app.database.optimizer import cleanup_old_records, get_database_stats
from app.logging_config import get_logger

logger = get_logger("db_scheduler")


class DatabaseScheduler:
    """데이터베이스 정리 작업 스케줄러"""

    def __init__(self, cleanup_interval_hours: int = 24, days_to_keep: int = 7):
        self.cleanup_interval_hours = cleanup_interval_hours
        self.days_to_keep = days_to_keep
        self.running = False
        self.task = None

    async def start(self):
        """스케줄러 시작"""
        if self.running:
            return

        self.running = True
        self.task = asyncio.create_task(self._scheduler_loop())
        logger.info(
            f"Database scheduler started "
            f"(cleanup every {self.cleanup_interval_hours}h, "
            f"keep {self.days_to_keep} days)"
        )

    async def stop(self):
        """스케줄러 정지"""
        if not self.running:
            return

        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Database scheduler stopped")

    async def _scheduler_loop(self):
        """스케줄러 메인 루프"""
        while self.running:
            try:
                # 데이터베이스 통계 로깅
                stats = get_database_stats()
                if stats:
                    logger.info(
                        f"DB Stats: {stats['total_records']} records, "
                        f"{stats['unique_servers']} servers, "
                        f"{stats['db_size_mb']}MB"
                    )

                # 정리 작업 수행
                deleted_count = cleanup_old_records(days_to_keep=self.days_to_keep)
                if deleted_count > 0:
                    logger.info(f"Cleanup completed: {deleted_count} records removed")

                # 다음 실행까지 대기
                await asyncio.sleep(self.cleanup_interval_hours * 3600)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in database scheduler: {e}")
                await asyncio.sleep(300)  # 5분 후 재시도


# 전역 스케줄러 인스턴스
_scheduler = None


def get_database_scheduler() -> DatabaseScheduler:
    """데이터베이스 스케줄러 인스턴스 획득"""
    global _scheduler
    if _scheduler is None:
        _scheduler = DatabaseScheduler()
    return _scheduler


async def start_database_scheduler():
    """데이터베이스 스케줄러 시작"""
    scheduler = get_database_scheduler()
    await scheduler.start()


async def stop_database_scheduler():
    """데이터베이스 스케줄러 정지"""
    global _scheduler
    if _scheduler:
        await _scheduler.stop()
        _scheduler = None
