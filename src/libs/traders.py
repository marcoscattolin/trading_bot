from lumibot.strategies.strategy import Strategy
from src.config.config import conf
from src.utils.logging import logger
from lumibot.brokers import Alpaca
from alpaca.trading.client import TradingClient

class AlpacaTrader(Strategy):

    name = "AlpacaTrader"

    broker = Alpaca({
            "API_KEY": conf.alpaca_creds.api_key,
            "API_SECRET": conf.alpaca_creds.secret_key.get_secret_value(),
            "PAPER": conf.alpaca_creds.paper,
        })

    def __init__(self):

        # call super
        super().__init__(broker=self.broker)
        self.initialize()


    def initialize(self):

        self.alpaca_client = TradingClient(
            api_key=conf.alpaca_creds.api_key,
            secret_key=conf.alpaca_creds.secret_key.get_secret_value(),
            paper=conf.alpaca_creds.paper
        )
        super().initialize()

    def get_cash(self):

        account = self.alpaca_client.get_account()
        cash = float(account.cash)
        logger.debug(f"[{self.name}]: Available cash for trading {cash}")

        return cash

    def position_sizing(self, symbol):
        """
        Calculate the quantity of shares to buy based on the cash at risk

        Returns:
        --------
        quantity: int
            The number of shares to buy
        """

        # keep some cash for avoiding day trading restrictions
        available_cash = 25_000 - self.get_cash()

        # max cash to use per trade
        if available_cash > 100:
            available_cash = 100
        else:
            available_cash = 0

        last_price = self.get_last_price(symbol)
        quantity = round(available_cash / last_price, 0)

        return available_cash, last_price, quantity


    def make_order(self, symbol, action):

        cash, last_price, quantity = self.position_sizing(symbol=symbol)

        if action == "buy":

            if quantity > 0:
                logger.debug(f"[{self.name}]: Position sizing: {quantity} shares of {symbol} at {last_price}")

                limit_price = round(last_price, 2)
                take_profit_price = round(last_price * 1.20, 2)
                stop_loss_price = round(last_price * .95, 2)

                order = self.create_order(
                    asset=symbol,
                    quantity=quantity,
                    time_in_force="gtc", # valid for today only
                    side="buy",
                    type="bracket",
                    # limit_price=limit_price,
                    take_profit_price=take_profit_price,
                    stop_loss_price=stop_loss_price
                )
                logger.info(f"[{self.name}]: Placing order {order}")
                self.submit_order(order)
            else:
                logger.info(f"[{self.name}]: Insufficient cash to buy {symbol} at {last_price}, implied quantity: {quantity}")

        elif action == "sell":
            # close positions
            position = self.alpaca_client.get_all_positions()
            for position in position:
                if position.symbol == symbol:
                    order = self.create_order(
                        asset=symbol,
                        quantity=position.qty,
                        side="sell",
                        type="market"
                    )
                    logger.info(f"[{self.name}]: Placing order: {order}")
                    self.submit_order(order)

            # cancel orders
            orders = self.alpaca_client.get_orders()
            for order in orders:
                if order.symbol == symbol:
                    logger.info(f"[{self.name}]: Cancelling order: {order}")
                    self.alpaca_client.cancel_order_by_id(order.id)
        else:
            logger.error(f"Invalid action: {action}")

    def close_all(self):
        """
        Close all positions and cancel all orders
        """
        self.alpaca_client.close_all_positions(cancel_orders=True)


if __name__ == "__main__":

    # init broker
    trader = AlpacaTrader()

    trader.make_order("AAPL", "buy")

    trader.make_order("AAPL", "sell")

    trader.make_order("TSLA", "sell")

    trader.close_all()