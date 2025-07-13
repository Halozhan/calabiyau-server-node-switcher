"""
Application configuration settings
"""

from typing import Optional


class Settings:
    """Application settings"""

    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # Database configuration
    DATABASE_PATH: str = "latency.db"

    # Crawler configuration
    CRAWLER_INTERVAL_MS: int = 100
    MAX_SERVERS_PER_REGION: int = 150
    DEFAULT_PORT: int = 20000

    # Server list configuration
    SERVER_LIST_PATH: str = "server_list.json"

    # Logging configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "logs/calabiyau.log"
    ENABLE_FILE_LOGGING: bool = True


settings = Settings()

# Global config for backward compatibility
config = {
    "interval_ms": settings.CRAWLER_INTERVAL_MS,
}
