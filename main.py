import socket
import time
from fastapi import FastAPI
from fastapi import Query

app = FastAPI()


@app.post("/query-ping")
async def query_ping(server_addr: str = Query(..., description="서버 주소 (IP:PORT)")):
    """
    UDP 방식으로 ping 테스트를 수행하고, 지연시간(ms)을 double(float)로 반환
    """
    try:
        ip, port = server_addr.split(":")
        port = int(port)
    except Exception:
        return {"error": "server_addr는 'IP:PORT' 형식이어야 합니다."}

    message = b"ping"
    timeout = 2.0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        start = time.perf_counter()
        sock.sendto(message, (ip, port))
        _data, _addr = sock.recvfrom(1024)
        end = time.perf_counter()
        latency_ms = (end - start) * 1000.0
        sock.close()
        return {"latency": latency_ms}
    except socket.timeout:
        return {"error": "Timeout: 서버로부터 응답이 없습니다."}
    except Exception as e:
        return {"error": str(e)}
