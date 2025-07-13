"""
Calabiyau Server Node Switcher - New Architecture Entry Point
기존 api_server.py와 같은 방식으로 실행 가능
"""

if __name__ == "__main__":
    import uvicorn
    from app.config import settings

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
