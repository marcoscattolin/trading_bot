from alpaca.data.live import NewsDataStream
from src.config.config import conf
from src.utils.logging import logger


class NewsListener:

    name = "NewsListener"

    def __init__(self, symbols:[str]):

        self.wss_client = NewsDataStream(
            api_key=conf.alpaca_creds.api_key,
            secret_key=conf.alpaca_creds.secret_key.get_secret_value()
        )
        self.wss_client.subscribe_news(self.handler, *symbols)

    async def handler(self, data):
        # convert data to dict
        message = dict(data)

        # log message
        logger.info(f"[{self.name}]: {message}")

        # send to dispatcher
        self.dispatch(message)

    def dispatch(self, message):

        # to be customized in inherited classes
        logger.debug(f"Will dispatch message: {message}")

    def run(self):
        self.wss_client.run()


if __name__ == "__main__":

    listener = NewsListener(symbols=["*"])
    listener.run()
