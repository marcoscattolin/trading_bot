from lumibot.backtesting import YahooDataBacktesting
from datetime import datetime
from src.utils.logging import logger
from src.bots.news_sentiment_trader import get_strategy

def backtest():

    strategy, params = get_strategy()

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
