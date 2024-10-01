from lumibot.backtesting import YahooDataBacktesting
from datetime import datetime
from src.utils.logging import logger
from src.bots.news_sentiment_trader import NewsSentimentTrader
from src.config.config import conf
from lumibot.brokers import Alpaca

def backtest():

    # retrieve backtest params
    params = {
            "symbol": conf.trading_bot.symbol,
            "cash_at_risk": conf.trading_bot.cash_at_risk,
            "sleeptime": conf.trading_bot.sleeptime,
            "api_key": conf.paper_creds.api_key,
            "secret_key": conf.paper_creds.secret_key.get_secret_value(),
            "base_url": conf.paper_creds.base_url
        }

    # init broker
    alpaca_config = {
        "API_KEY": params["api_key"],
        "API_SECRET": params["secret_key"],
        "PAPER": True,
    }
    broker = Alpaca(alpaca_config)

    # init strategy
    strategy = NewsSentimentTrader(
        name="NewsSentimentTrader",
        broker=broker,
        parameters=params
    )
    logger.info(f"Initializing {strategy.name} with params: {params}")

    # backtest
    start = datetime(2023, 12, 1)
    end = datetime(2023, 12, 31)
    logger.info(f"Backtesting {strategy.name}: backtest period from {start} to {end}")
    strategy.backtest(
        YahooDataBacktesting,
        start,
        end,
        parameters=params
    )


if __name__ == "__main__":
    backtest()
