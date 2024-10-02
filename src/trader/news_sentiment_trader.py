from lumibot.strategies.strategy import Strategy
from src.utils.logging import logger
from src.config.config import broker, conf

class NewsSentimentTrader(Strategy):

    def initialize(self, my_param):

        self.my_param = my_param


if __name__ == "__main__":

    from lumibot.backtesting import YahooDataBacktesting

    params = {
        "my_param": 100000
    }
    logger.info("Initializing trader...")
    trader = NewsSentimentTrader(
        broker=broker,
        parameters=params

    )

    start = conf.trading_bot.backtest_start
    end = conf.trading_bot.backtest_end
    trader.backtest(YahooDataBacktesting, start, end, parameters=params)
    logger.info(f"Success {trader.my_param}")