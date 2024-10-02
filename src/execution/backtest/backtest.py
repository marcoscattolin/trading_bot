from lumibot.backtesting import YahooDataBacktesting
from datetime import datetime
from src.strategies.golden_cross import GoldenCross
from lumibot.brokers import Alpaca
from src.config.config import conf

def backtest():

    # init alpaca broker
    ALPACA_CONFIG = {
        "API_KEY": conf.alpaca_creds.api_key,
        "API_SECRET": conf.alpaca_creds.secret_key.get_secret_value(),
        "PAPER": conf.alpaca_creds.paper  # Set to True for paper trading, False for live trading
    }

    params = {
            "symbol": conf.trading_bot.symbol,
            "short_window": 7,
            "long_window": 14,
            "cash_at_risk": conf.trading_bot.cash_at_risk,
            "sleeptime": conf.trading_bot.sleeptime,
        }

    # Pick the dates that you want to start and end your backtest
    backtesting_start = datetime(2024, 1, 1)
    backtesting_end = datetime(2024, 1, 31)

    # init broker
    broker = Alpaca(ALPACA_CONFIG)
    strategy = GoldenCross(broker=broker, parameters=params)

    # Run the backtest
    strategy.backtest(
        YahooDataBacktesting,
        backtesting_start,
        backtesting_end,
        parameters=params,
    )


if __name__ == "__main__":
    backtest()
