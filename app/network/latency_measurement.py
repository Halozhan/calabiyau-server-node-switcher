"""
Latency measurement module using UDP ping
"""

import aioudp
import asyncio
import time
from typing import Dict, Union
from app.logging_config import get_logger

logger = get_logger("latency_measurement")


async def measure_latency(
    server_addr: str, port: int = 20000, timeout: float = 1.0
) -> Dict[str, Union[float, str]]:
    """
    UDP 방식으로 ping 테스트를 수행하고, 지연시간(ms)을 반환

    Args:
        server_addr: 서버 IP 주소
        port: 서버 포트 (기본값: 20000)
        timeout: 타임아웃 시간(초) (기본값: 1.0)

    Returns:
        성공 시: {"latency": float} (ms 단위)
        실패 시: {"error": str}
    """
    message = b"a"

    try:
        async with aioudp.connect(server_addr, port) as connection:
            start = time.perf_counter()
            await connection.send(message)

            # 응답 대기
            response = await asyncio.wait_for(connection.recv(), timeout=timeout)
            end = time.perf_counter()

            if response == message:
                latency_ms = (end - start) * 1000.0
                return {"latency": latency_ms}
            else:
                return {"error": "Invalid response from server"}

    except asyncio.TimeoutError:
        return {"error": f"Timeout: No response from {server_addr}:{port}"}
    except ConnectionRefusedError:
        return {"error": f"Connection refused to {server_addr}:{port}"}
    except OSError as e:
        return {"error": f"Network error: {e}"}
    except Exception as e:
        logger.error(f"Unexpected error measuring latency to {server_addr}:{port}: {e}")
        return {"error": f"Unexpected error: {e}"}


async def measure_multiple_latencies(
    servers: list, port: int = 20000, timeout: float = 1.0, max_concurrent: int = 50
) -> Dict[str, Dict[str, Union[float, str]]]:
    """
    여러 서버에 대해 동시에 latency 측정

    Args:
        servers: 서버 주소 리스트
        port: 포트 번호
        timeout: 타임아웃 시간
        max_concurrent: 최대 동시 연결 수

    Returns:
        서버별 latency 결과 딕셔너리
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def measure_with_semaphore(server_addr: str):
        async with semaphore:
            result = await measure_latency(server_addr, port, timeout)
            return server_addr, result

    tasks = [measure_with_semaphore(server) for server in servers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    latency_results = {}
    for result in results:
        if isinstance(result, tuple):
            server_addr, latency_data = result
            latency_results[server_addr] = latency_data
        elif isinstance(result, Exception):
            logger.error(f"Error in concurrent latency measurement: {result}")

    return latency_results


# 하위 호환성을 위한 별칭
query_ping = measure_latency


if __name__ == "__main__":
    # 테스트 예제
    async def test_latency():
        test_servers = ["8.8.8.8", "1.1.1.1"]

        # 단일 서버 테스트
        result = await measure_latency("8.8.8.8", 53)  # DNS 포트
        print(f"Single test result: {result}")

        # 다중 서버 테스트
        results = await measure_multiple_latencies(test_servers, 53)
        print(f"Multiple test results: {results}")

    asyncio.run(test_latency())
