from lumibot.traders import Trader
from src.bots.news_sentiment_trader import NewsSentimentTrader
from lumibot.brokers import Alpaca
from src.utils.logging import logger
from src.config.config import conf

def deploy():

    # retrieve live params
    params = {
            "symbol": conf.trading_bot.symbol,
            "cash_at_risk": conf.trading_bot.cash_at_risk,
            "sleeptime": conf.trading_bot.sleeptime,
            "api_key": conf.paper_creds.api_key,
            "secret_key": conf.paper_creds.secret_key.get_secret_value(),
            "base_url": conf.paper_creds.base_url
        }

    # init broker on
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

    # deploy
    logger.info(f"Deploying {strategy.name} on Paper Market")
    trader = Trader()
    trader.add_strategy(strategy)
    trader.run_all()

if __name__ == "__main__":
    deploy()
