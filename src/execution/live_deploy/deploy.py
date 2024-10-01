from lumibot.traders import Trader
from src.bots.news_sentiment_trader import NewsSentimentTrader
from lumibot.brokers import Alpaca
from src.utils.logging import logger
from src.config.config import conf

def deploy():

    # init broker on
    alpaca_config = {
        "API_KEY": conf.live_creds.api_key,
        "API_SECRET": conf.live_creds.secret_key.get_secret_value(),
        "PAPER": True,
    }
    broker = Alpaca(alpaca_config)

    # init strategy
    params = {
            "symbol": conf.trading_bot.symbol,
            "cash_at_risk": conf.trading_bot.cash_at_risk,
            "sleeptime": conf.trading_bot.sleeptime
        }
    strategy = NewsSentimentTrader(
        name="NewsSentimentTrader",
        broker=broker,
        parameters=params
    )
    logger.info(f"Initializing {strategy.name} with params: {params}")

    # deploy
    logger.critical(f"Deploying {strategy.name} on Live Market")
    trader = Trader()
    trader.add_strategy(strategy)
    trader.run_all()

if __name__ == "__main__":
    deploy()
