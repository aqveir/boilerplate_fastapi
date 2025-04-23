import uvicorn

# Import config
from modules.base.config import config


def start_server():
    # print('Starting Server...')       
    uvicorn.run(
        app="server.start:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        log_level="debug" if config.ENVIRONMENT != "production" else "info",
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1 if config.ENVIRONMENT != "production" else 4,
    )
    # webbrowser.open("http://127.0.0.1:8080")
    # uvicorn server.main:app --host 0.0.0.0 --port 8080

if __name__ == "__main__":
    start_server()