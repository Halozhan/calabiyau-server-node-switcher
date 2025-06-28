import socket
import time


async def query_ping(server_addr: str, port: int = 20000) -> dict:
    """
    UDP 방식으로 ping 테스트를 수행하고, 지연시간(ms)을 double(float)로 반환
    """
    message = b"ping"
    timeout = 0.5
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        start = time.perf_counter()
        sock.sendto(message, (server_addr, port))
        _data, _addr = sock.recvfrom(1024)
        end = time.perf_counter()
        latency_ms = (end - start) * 1000.0
        sock.close()
        return {"latency": latency_ms}
    except socket.timeout:
        return {"error": "Timeout: 서버로부터 응답이 없습니다."}
    except Exception as e:
        return {"error": str(e)}
