import asyncio
from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, Query
from latency_crawler.query_ping import query_ping
from timeseries_db import get_latency_stats
from typing import Optional
import uvicorn
import sqlite3
from dns_query.query_servers import query_server
import json


async def init_db():
    """
    데이터베이스 초기화 함수
    """
    conn = sqlite3.connect("latency.db")
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


@asynccontextmanager
async def crawling_task(app: FastAPI):
    # DB 초기화
    await init_db()

    # region 정보 로드
    server_list = json.load(open("server_list.json", "r", encoding="utf-8"))

    # DNS 쿼리 수행
    for region, info in server_list.items():
        print(f"쿼리 중: {region} - {info['domain']}")
        for i in range(1, 151):  # 최대 150개 서버 쿼리
            domain = info["domain"].replace("{iterable}", str(i))
            print(f"쿼리 도메인: {domain}")
            try:
                # 쿼리 결과를 저장
                results = await query_server(domain)
                if "nodes" not in info:
                    info["nodes"] = []
                info["nodes"].append({domain: results})
                print(f"쿼리 결과: {results}")
            except Exception as e:
                print(f"쿼리 실패: {domain} - {e}")
                # 쿼리 실패 시 이후에 더 이상 서버가 없다고 가정하고 탈출
                break

    print("모든 서버 쿼리 완료")
    print(server_list)

    # ping worker
    async def ping_worker(region: str, domain: str, ip: str, port: int):
        result = await query_ping(ip, port=port)
        # 결과를 DB에 저장

        conn = sqlite3.connect("latency.db")
        c = conn.cursor()
        if "latency" in result:
            # 성공
            # print(f"{domain} - {ip}:{port}: {result['latency']:.2f} ms (성공)")
            c.execute(
                "INSERT INTO latency (region, domain, server_addr, port, latency, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (region, domain, ip, port, result["latency"], int(time.time())),
            )
        else:
            print(f"{domain} - {ip}:{port}: 실패: {result}")
            c.execute(
                "INSERT INTO latency (region, domain, server_addr, port, latency, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (region, domain, ip, port, -1.0, int(time.time())),
            )
        conn.commit()

    # 백그라운드 태스크 정의
    async def background_crawl():
        try:
            while True:
                tasks = []
                # 모든 nodes의 IP에 대해 ping을 수행하는 작업
                for region, info in server_list.items():
                    for node in info.get("nodes", []):
                        for domain, ips in node.items():
                            for ip in ips:
                                # IP와 포트(20000)로 핑 작업을 수행하는 태스크 생성
                                tasks.append(
                                    asyncio.create_task(
                                        ping_worker(
                                            region, domain, ip, info.get("port", 20000)
                                        )
                                    )
                                )

                # 모든 핑 작업이 완료될 때까지 대기
                # result = await asyncio.gather(*tasks, return_exceptions=False)
                # print(result)
                await asyncio.sleep(config["interval_ms"] / 1000)
                print("크롤링 작업 수행 중...")
                # 크롤링 작업 수행
                pass
        except asyncio.CancelledError:
            print("크롤링 작업이 취소되었습니다.")

    # 백그라운드 태스크 실행
    task = asyncio.create_task(background_crawl())

    try:
        yield  # 서버가 살아있는 동안 여기서 대기
    finally:
        task.cancel()
        await task


app = FastAPI(lifespan=crawling_task)
config = {
    "interval_ms": 100,
}


# 새로고침 주기 설정
@app.get("/api/config")
def get_config():
    """
    클라이언트가 interval_ms를 요청할 때 사용
    """
    return {"interval_ms": config["interval_ms"]}


@app.post("/api/config")
def set_config(interval_ms: Optional[int] = Query(None)):
    """
    클라이언트가 interval_ms를 설정할 때 사용
    """
    if interval_ms is not None:
        config["interval_ms"] = interval_ms
    return {"interval_ms": config["interval_ms"]}


@app.get("/api/stats")
def stats(
    region: str = Query(...), server_addr: str = Query(...), window: int = Query(30)
):
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
    return [{"region": row[0], "server_addr": row[1]} for row in rows]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
