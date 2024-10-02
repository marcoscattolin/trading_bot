from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient, NewsClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest, NewsRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
from src.config.config import conf
from src.utils.logging import logger



def query_crypto():

    logger.info("Getting crypto data")

    client = CryptoHistoricalDataClient()
    request_params = CryptoBarsRequest(
                            symbol_or_symbols=["BTC/USD", "ETH/USD"],
                            timeframe=TimeFrame.Day,
                            start="2022-07-01"
                     )

    bars = client.get_crypto_bars(request_params)
    logger.info(f"Bars: {bars}")

def query_stock():

    logger.info("Getting stock data")

    stock_client = StockHistoricalDataClient(api_key=conf.alpaca_creds.api_key, secret_key=conf.alpaca_creds.secret_key.get_secret_value())
    request_params = StockBarsRequest(
                            symbol_or_symbols=["AAPL"],
                            timeframe=TimeFrame.Day,
                            start="2022-07-01"
                     )
    bars = stock_client.get_stock_bars(request_params)

    logger.info(f"Bars: {bars}")

def query_last_quote():

    logger.info("Getting last quote")

    stock_client = StockHistoricalDataClient(api_key=conf.alpaca_creds.api_key, secret_key=conf.alpaca_creds.secret_key.get_secret_value())
    quote_request = StockLatestQuoteRequest(symbol_or_symbols="AAPL")
    quote = stock_client.get_stock_latest_quote(quote_request)

    logger.info(f"Quote: {quote}")

def query_news():

    logger.info("Getting news")

    news_client = NewsClient(api_key=conf.alpaca_creds.api_key, secret_key=conf.alpaca_creds.secret_key.get_secret_value())
    request_params = NewsRequest(
        symbols="AAPL",
        start="2022-07-01",
        end="2022-07-10"
    )
    news = news_client.get_news(request_params)
    logger.info(f"News: {news}")

def run():

    query_crypto()
    query_stock()
    query_last_quote()
    query_news()


if __name__ == "__main__":

    run()
