from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.brokers import Alpaca
from lumibot.traders import Trader
from src.config.config import conf
from src.utils.logging import logger

# A simple strategy that buys AAPL on the first day and holds it
class MyStrategy(Strategy):

    def on_trading_iteration(self):

        if self.first_iteration:

            quantity = 1

            logger.warning(f"First iteration, buying AAPL, qty: {quantity}")
            order = self.create_order(asset="AAPL", quantity=quantity, side="buy")
            self.submit_order(order)

        else:
            logger.info("Not first iteration, passing")
            pass


def backtest():
    # Pick the dates that you want to start and end your backtest
    backtesting_start = datetime(2020, 11, 1)
    backtesting_end = datetime(2020, 12, 31)

    # Run the backtest
    MyStrategy.backtest(
        YahooDataBacktesting,
        backtesting_start,
        backtesting_end,
    )

def live_trade():

    ALPACA_CONFIG = {
     "API_KEY": conf.alpaca_creds.api_key,
     "API_SECRET": conf.alpaca_creds.secret_key.get_secret_value(),
     "PAPER": conf.alpaca_creds.paper  # Set to True for paper trading, False for live trading
    }

    # Run the live trading bot
    trader = Trader()
    broker = Alpaca(ALPACA_CONFIG)
    strategy = MyStrategy(broker=broker)

    trader.add_strategy(strategy)
    trader.run_all()

if __name__ == "__main__":
    live_trade()
