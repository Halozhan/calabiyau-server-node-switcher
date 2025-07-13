"""
Background tasks and workers
"""

import asyncio
from contextlib import asynccontextmanager
from app.database.models import init_db
from app.services.crawler_service import discover_servers
from app.services.ping_service import ping_all_servers
from app.config import config


@asynccontextmanager
async def background_crawl_manager():
    """
    Context manager for background crawling tasks
    """
    # DB 초기화
    await init_db()

    # 서버 발견
    server_list = await discover_servers()
    print(f"발견된 서버 목록: {server_list}")

    # 백그라운드 태스크 정의
    async def background_crawl():
        try:
            while True:
                print("크롤링 작업 수행 중...")

                # 모든 서버에 대해 핑 테스트 수행
                await ping_all_servers(server_list)

                # 설정된 간격만큼 대기
                await asyncio.sleep(config["interval_ms"] / 1000)

        except asyncio.CancelledError:
            print("크롤링 작업이 취소되었습니다.")

    # 백그라운드 태스크 실행
    task = asyncio.create_task(background_crawl())

    try:
        yield {"task": task, "server_list": server_list}
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
