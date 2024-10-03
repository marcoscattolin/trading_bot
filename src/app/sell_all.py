from lumibot.strategies.strategy import Strategy
from src.config.config import conf
from src.utils.logging import logger
from lumibot.brokers import Alpaca
from alpaca.trading.client import TradingClient
from src.app.traders import AlpacaTrader

if __name__ == "__main__":

    # init broker
    alpaca_config = {
        "API_KEY": conf.alpaca_creds.api_key,
        "API_SECRET": conf.alpaca_creds.secret_key.get_secret_value(),
        "PAPER": conf.alpaca_creds.paper,
    }
    broker = Alpaca(alpaca_config)

    trader = AlpacaTrader(broker=broker)

    trader.initialize()

    logger.warning("Selling all positions and canceling all orders...")
    trader.alpaca_client.close_all_positions(cancel_orders=True)
    logger.warning("All positions sold.")
