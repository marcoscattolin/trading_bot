from lumibot.strategies.strategy import Strategy
from src.config.config import conf
from src.utils.logging import logger
from lumibot.brokers import Alpaca
from alpaca.trading.client import TradingClient

class AlpacaTrader(Strategy):

    def initialize(self, cash_at_risk:float = 0.5):

        self.alpaca_client = TradingClient(
            api_key=conf.alpaca_creds.api_key,
            secret_key=conf.alpaca_creds.secret_key.get_secret_value(),
            paper=conf.alpaca_creds.paper
        )

    def sell_all(self):

        # close positions
        positions = self.get_positions()
        for position in positions:
            order = self.create_order(
                asset=position.symbol,
                quantity=position.quantity,
                side="sell",
                type="market"
            )
            logger.debug(f"Placing order: {order}")
            self.submit_order(order)

        # close orders
        orders = self.get_orders()
        for order in orders:
            logger.debug(f"Cancelling order: {order}")
            self.cancel_order(order)


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

    trader.sell_all()
