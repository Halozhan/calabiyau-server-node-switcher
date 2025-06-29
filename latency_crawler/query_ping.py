import aioudp
import asyncio
import time


async def query_ping(server_addr: str, port: int = 20000) -> dict:
    """
    UDP 방식으로 ping 테스트를 수행하고, 지연시간(ms)을 double(float)로 반환 (aioudp 기반 비동기)
    """
    message = b"a"
    timeout = 1.0

    async with aioudp.connect(server_addr, port) as connection:
        try:
            start = time.perf_counter()
            await connection.send(message)
            assert await asyncio.wait_for(connection.recv(), timeout=timeout) == message
            end = time.perf_counter()
            latency_ms = (end - start) * 1000.0
            return {"latency": latency_ms}
        except Exception:
            return {"error": "Timeout: 서버로부터 응답이 없습니다."}
