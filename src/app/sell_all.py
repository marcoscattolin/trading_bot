from src.utils.logging import logger
from src.app.traders import AlpacaTrader

if __name__ == "__main__":

    logger.info("Closing all positions")
    trader = AlpacaTrader()
    trader.close_all()
    logger.info("All positions closed")
