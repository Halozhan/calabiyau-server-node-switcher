"""
Main FastAPI application entry point
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from app.config import settings
from app.api.routes import router
from app.background.tasks import background_crawl_manager
from app.database.batch_writer import get_batch_writer, stop_batch_writer
from app.database.scheduler import start_database_scheduler, stop_database_scheduler
from app.logging_config import setup_logging, get_logger

# Initialize logging
logger = setup_logging(
    level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE if settings.ENABLE_FILE_LOGGING else None,
)
app_logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    app_logger.info("🚀 Starting Calabiyau Server Node Switcher...")

    # Startup
    try:
        # 배치 라이터 시작
        get_batch_writer()  # 인스턴스 생성 및 시작
        app_logger.info("✅ Batch writer started successfully")

        # 데이터베이스 스케줄러 시작
        await start_database_scheduler()
        app_logger.info("✅ Database scheduler started successfully")

        async with background_crawl_manager() as manager:
            app.state.crawler = manager
            app_logger.info("✅ Background crawler started successfully")
            yield
    except Exception as e:
        app_logger.error(f"❌ Failed to start services: {e}")
        raise
    finally:
        # 정리 작업
        await stop_database_scheduler()
        stop_batch_writer()
        app_logger.info("🛑 Shutting down application...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Calabiyau Server Node Switcher",
        description="Server latency monitoring and switching service",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Include API routes
    app.include_router(router, prefix="/api")

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG
    )
