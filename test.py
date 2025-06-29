import asyncio
import time
from latency_crawler.query_ping import query_ping


async def ping_loop(ip: str, port: int = 20000, interval_ms: int = 100):
    print(f"{ip}:{port}에 100ms 간격으로 무한 ping 시작...")
    loop = asyncio.get_event_loop()
    pending = set()
    count = 0
    try:
        while True:
            # 100ms마다 새로운 ping 태스크 추가
            pending.add(loop.create_task(query_ping(ip, port)))
            await asyncio.sleep(interval_ms / 1000.0)
            # 완료된 태스크는 바로 결과 출력
            done, pending = await asyncio.wait(
                pending, timeout=0, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                count += 1
                result = task.result()
                if isinstance(result, dict) and "latency" in result:
                    print(f"{count}번째: {result['latency']:.2f} ms (성공)")
                else:
                    print(f"{count}번째: 실패: {result}")
    except KeyboardInterrupt:
        print("중단됨")


if __name__ == "__main__":
    asyncio.run(ping_loop("118.24.57.146", 20000, 100))
