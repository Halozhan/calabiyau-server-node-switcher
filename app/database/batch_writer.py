"""
배치 처리를 위한 데이터베이스 라이터
"""

import sqlite3
import time
import threading
from typing import List, Optional
from queue import Queue
from dataclasses import dataclass
from app.config import settings
from app.logging_config import get_logger

logger = get_logger("batch_writer")


@dataclass
class LatencyRecord:
    """레이턴시 레코드 데이터 클래스"""

    region: str
    domain: str
    server_addr: str
    port: int
    latency: float
    timestamp: int


class BatchWriter:
    """배치 처리를 위한 데이터베이스 라이터"""

    def __init__(
        self,
        db_path: Optional[str] = None,
        batch_size: int = 50,
        flush_interval: float = 5.0,
        max_queue_size: int = 1000,
    ):
        self.db_path = db_path or settings.DATABASE_PATH
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.max_queue_size = max_queue_size

        self.queue = Queue(maxsize=max_queue_size)
        self.batch_buffer: List[LatencyRecord] = []
        self.last_flush_time = time.time()
        self.running = False
        self.worker_thread = None

        # 연결 풀링을 위한 연결 객체
        self._connection = None
        self._connection_lock = threading.Lock()

    def start(self):
        """배치 라이터 시작"""
        if self.running:
            return

        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        logger.info(
            f"BatchWriter started with batch_size={self.batch_size}, "
            f"flush_interval={self.flush_interval}s"
        )

    def stop(self):
        """배치 라이터 정지 및 남은 데이터 플러시"""
        if not self.running:
            return

        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=10)

        # 남은 데이터 플러시
        self._flush_batch()
        self._close_connection()
        logger.info("BatchWriter stopped")

    def add_record(
        self, region: str, domain: str, server_addr: str, port: int, latency: float
    ) -> bool:
        """레코드를 큐에 추가"""
        try:
            record = LatencyRecord(
                region=region,
                domain=domain,
                server_addr=server_addr,
                port=port,
                latency=latency,
                timestamp=int(time.time()),
            )
            self.queue.put_nowait(record)
            return True
        except Exception as e:
            logger.warning(f"Failed to add record to queue: {e}")
            return False

    def _get_connection(self) -> sqlite3.Connection:
        """연결 풀링을 위한 연결 획득"""
        with self._connection_lock:
            if self._connection is None:
                self._connection = sqlite3.connect(
                    self.db_path, check_same_thread=False, timeout=30.0
                )
                # WAL 모드 활성화 (동시성 향상)
                self._connection.execute("PRAGMA journal_mode=WAL")
                # 동기화 모드 변경 (성능 향상)
                self._connection.execute("PRAGMA synchronous=NORMAL")
                # 캐시 크기 증가
                self._connection.execute("PRAGMA cache_size=10000")
            return self._connection

    def _close_connection(self):
        """연결 닫기"""
        with self._connection_lock:
            if self._connection:
                self._connection.close()
                self._connection = None

    def _worker(self):
        """백그라운드 워커 스레드"""
        while self.running:
            try:
                # 큐에서 레코드 가져오기 (타임아웃 사용)
                try:
                    record = self.queue.get(timeout=1.0)
                    self.batch_buffer.append(record)
                except Exception:
                    # 타임아웃 발생 시 계속 진행
                    pass

                # 배치 플러시 조건 확인
                current_time = time.time()
                time_exceeded = (
                    current_time - self.last_flush_time >= self.flush_interval
                )
                should_flush = len(self.batch_buffer) >= self.batch_size or (
                    self.batch_buffer and time_exceeded
                )

                if should_flush:
                    self._flush_batch()

            except Exception as e:
                logger.error(f"Error in batch writer worker: {e}")
                time.sleep(1.0)

    def _flush_batch(self):
        """배치 데이터를 데이터베이스에 기록"""
        if not self.batch_buffer:
            return

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # 배치 INSERT 수행
            records_data = [
                (r.region, r.domain, r.server_addr, r.port, r.latency, r.timestamp)
                for r in self.batch_buffer
            ]

            cursor.executemany(
                """
                INSERT INTO latency (region, domain, server_addr, port, latency, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                records_data,
            )

            conn.commit()

            logger.debug(f"Flushed {len(self.batch_buffer)} records to database")
            self.batch_buffer.clear()
            self.last_flush_time = time.time()

        except Exception as e:
            logger.error(f"Failed to flush batch to database: {e}")
            # 실패 시 연결 재설정
            self._close_connection()


# 전역 배치 라이터 인스턴스
_batch_writer = None


def get_batch_writer() -> BatchWriter:
    """배치 라이터 인스턴스 획득"""
    global _batch_writer
    if _batch_writer is None:
        _batch_writer = BatchWriter()
        _batch_writer.start()
    return _batch_writer


def stop_batch_writer():
    """배치 라이터 정지"""
    global _batch_writer
    if _batch_writer:
        _batch_writer.stop()
        _batch_writer = None
