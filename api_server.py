from fastapi import FastAPI, Query
from timeseries_db import get_latency_stats
from typing import Optional
import uvicorn
import sqlite3

app = FastAPI()

@app.get("/api/stats")
def stats(region: str = Query(...), server_addr: str = Query(...), window: int = Query(30)):
    """
    region, server_addr, window(초)로 최근 통계 반환
    """
    return get_latency_stats(region, server_addr, window)

@app.get("/api/servers")
def get_all_servers():
    """
    DB에서 region, server_addr의 유니크 쌍을 모두 반환
    """
    conn = sqlite3.connect("latency.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT region, server_addr FROM latency")
    rows = c.fetchall()
    conn.close()
    return [ {"region": row[0], "server_addr": row[1]} for row in rows ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
