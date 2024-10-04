from alpaca.data.live import NewsDataStream
from src.utils.logging import logger
import os

class NewsListener:

    name = "NewsListener"

    def __init__(self, symbols:[str]):

        self.wss_client = NewsDataStream(
            api_key=os.getenv("ALPACA_API_KEY"),
            secret_key=os.getenv("ALPACA_SECRET_KEY"),
        )
        self.wss_client.subscribe_news(self.handler, *symbols)

    async def handler(self, data):
        # convert data to dict
        message = dict(data)

        # log message
        logger.debug(f"[{self.name}]: {message}")

        # send to dispatcher
        self.dispatch(message)

    def dispatch(self, message):

        # to be customized in inherited classes
        logger.debug(f"[{self.name}] will dispatch message: {message}")

    def run(self):
        self.wss_client.run()


if __name__ == "__main__":

    listener = NewsListener(symbols=["*"])
    listener.run()
