import sqlite3
import time
from typing import Optional


# def init_db(db_path: str = "latency.db"):
#     conn = sqlite3.connect(db_path)
#     c = conn.cursor()
#     c.execute(
#         """
#         CREATE TABLE IF NOT EXISTS latency (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             region TEXT,
#             server_addr TEXT,
#             latency REAL,
#             success INTEGER,
#             timestamp INTEGER
#         )
#     """
#     )
#     conn.commit()
#     conn.close()


def insert_latency(
    region: str,
    server_addr: str,
    latency: float,
    success: int,
    db_path: str = "latency.db",
):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO latency (region, server_addr, latency, success, timestamp) VALUES (?, ?, ?, ?, ?)",
        (region, server_addr, latency, success, int(time.time())),
    )
    conn.commit()
    conn.close()


def get_latency(region: Optional[str] = None, db_path: str = "latency.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if region:
        c.execute(
            "SELECT * FROM latency WHERE region = ? ORDER BY timestamp DESC", (region,)
        )
    else:
        c.execute("SELECT * FROM latency ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def get_latency_stats(
    region: str, server_addr: str, window: int = 30, db_path: str = "latency.db"
):
    """
    최근 window(초)간의 평균, 최소, 최대, 손실률, 측정 개수 반환
    """
    now = int(time.time())
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        SELECT latency FROM latency
        WHERE region = ? AND server_addr = ? AND timestamp >= ?
        ORDER BY timestamp DESC
        """,
        (region, server_addr, now - window),
    )
    rows = c.fetchall()
    conn.close()

    # latency가 0보다 큰 것만 성공으로 간주
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

    # raw_data도 추가하여 차트에서 사용할 수 있도록
    raw_data = []
    if rows:
        # 최근 데이터부터 timestamp와 함께 반환
        c2 = sqlite3.connect(db_path)
        c2_cursor = c2.cursor()
        c2_cursor.execute(
            """
            SELECT timestamp, latency FROM latency
            WHERE region = ? AND server_addr = ? AND timestamp >= ?
            ORDER BY timestamp ASC
            """,
            (region, server_addr, now - window),
        )
        raw_rows = c2_cursor.fetchall()
        c2.close()
        raw_data = [{"timestamp": row[0], "latency": row[1]} for row in raw_rows]

    return {
        "avg": avg,
        "min": min_latency,
        "max": max_latency,
        "loss_rate": loss_rate,
        "count": count,
        "raw_data": raw_data,
    }


if __name__ == "__main__":
    pass
