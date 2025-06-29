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
        SELECT latency, success FROM latency
        WHERE region = ? AND server_addr = ? AND timestamp >= ?
        ORDER BY timestamp DESC
        """,
        (region, server_addr, now - window),
    )
    rows = c.fetchall()
    conn.close()
    latencies = [row[0] for row in rows if row[1] == 1]
    count = len(rows)
    loss_count = sum(1 for row in rows if row[1] == 0)
    loss_rate = loss_count / count if count > 0 else None
    avg = sum(latencies) / len(latencies) if latencies else None
    min_latency = min(latencies) if latencies else None
    max_latency = max(latencies) if latencies else None
    return {
        "avg": avg,
        "min": min_latency,
        "max": max_latency,
        "loss_rate": loss_rate,
        "count": count,
    }


if __name__ == "__main__":
    init_db()
