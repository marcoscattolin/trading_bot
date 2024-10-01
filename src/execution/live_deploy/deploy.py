from src.utils.logging import logger
from lumibot.traders import Trader
from src.bots.news_sentiment_trader import get_strategy

def deploy():

    strategy, params = get_strategy()

    # deploy
    logger.critical(f"Deploying {strategy.name} on Live Market")
    trader = Trader()
    trader.add_strategy(strategy)
    trader.run_all()

if __name__ == "__main__":
    deploy()
