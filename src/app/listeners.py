from alpaca.data.live import NewsDataStream
from src.config.config import conf
from src.app.handlers import LLMTradingHandler as Handler
from src.utils.logging import logger


class NewsListener:

    def __init__(self, handle_func, symbols:[str]):

        self.wss_client = NewsDataStream(
            api_key=conf.alpaca_creds.api_key,
            secret_key=conf.alpaca_creds.secret_key.get_secret_value()
        )
        self.wss_client.subscribe_news(handle_func, *symbols)

    def run(self):
        self.wss_client.run()


if __name__ == "__main__":

    logger.setLevel("WARNING")
    handler = Handler().get_handler()
    listener = NewsListener(handler, symbols=["*"])
    listener.run()
