""" Import the required modules """
import webbrowser
import uvicorn

# Import config
from modules.base.config import config


def start_server():
    """ Start the Uvicorn server """
    # print('Starting Server...')
    uvicorn.run(
        app="server.start:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        log_level="debug" if config.ENVIRONMENT != "production" else "info",
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1 if config.ENVIRONMENT != "production" else 4,
    )

    # Open the browser automatically
    # webbrowser.open("http://127.0.0.1:"+str(config.APP_PORT), new=2)

if __name__ == "__main__":
    start_server()
