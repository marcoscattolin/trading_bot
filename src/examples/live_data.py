from alpaca.data.live import StockDataStream, CryptoDataStream, NewsDataStream
from src.config.config import conf


# async handler
async def data_handler(data):
    # quote data will arrive here
    print(data)

def live_stock():

    wss_client = StockDataStream(api_key=conf.alpaca_creds.api_key, secret_key=conf.alpaca_creds.secret_key.get_secret_value())
    wss_client.subscribe_quotes(data_handler, "SPY")
    wss_client.run()

def live_crypto():

    wss_client = CryptoDataStream(api_key=conf.alpaca_creds.api_key, secret_key=conf.alpaca_creds.secret_key.get_secret_value())
    wss_client.subscribe_quotes(data_handler, "BTC/USD")
    wss_client.run()

def live_news():

        wss_client = NewsDataStream(api_key=conf.alpaca_creds.api_key, secret_key=conf.alpaca_creds.secret_key.get_secret_value())
        wss_client.subscribe_news(data_handler, "*")
        wss_client.run()

if __name__ == "__main__":

    live_stock()
    #live_crypto()
    #live_news()