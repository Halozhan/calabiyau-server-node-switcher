import asyncio
import time
from dns_query.query_servers import query_servers
from latency_crawler.query_ping import query_ping
from timeseries_db import init_db, insert_latency


async def monitor_all_regions(regions, interval=1):
    # DB 초기화
    init_db()
    # 서버 리스트 수집
    server_lists = await asyncio.gather(
        *[
            query_servers(region_code, region_name)
            for region_name, region_code in regions
        ]
    )
    # (region_name, server_addr) 튜플 리스트 생성
    region_server_pairs = []
    for (region_name, _), servers in zip(regions, server_lists):
        for server in servers:
            region_server_pairs.append((region_name, server))
    print(f"모니터링 대상 서버 수: {len(region_server_pairs)}")

    # 매 interval(초)마다 모든 서버에 대해 10번씩 ping
    while True:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Ping 측정 시작")
        for region_name, server_addr in region_server_pairs:
            ping_tasks = [query_ping(server_addr) for _ in range(10)]
            results = await asyncio.gather(*ping_tasks)
            for result in results:
                if isinstance(result, dict) and "latency" in result:
                    latency = result["latency"]
                    success = 1
                    insert_latency(region_name, server_addr, latency, success)
                    print(f"{region_name} {server_addr} -> {latency:.2f} ms (성공)")
                else:
                    latency = -1.0
                    success = 0
                    insert_latency(region_name, server_addr, latency, success)
                    print(f"{region_name} {server_addr} -> 실패: {result}")
        await asyncio.sleep(interval)


if __name__ == "__main__":
    regions = [
        ("成都, Chengdu", "cd"),
        ("北京, Beijing", "bj"),
        ("南京, Nanjing", "nj"),
        ("广州, Guangzhou", "gz"),
    ]
    asyncio.run(monitor_all_regions(regions, interval=1))
