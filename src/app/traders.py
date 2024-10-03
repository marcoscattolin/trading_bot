from lumibot.strategies.strategy import Strategy
from src.config.config import conf
from src.utils.logging import logger
from lumibot.brokers import Alpaca
from alpaca.trading.client import TradingClient

class AlpacaTrader(Strategy):

    def initialize(self, cash_at_risk:float = 0.5):

        self.cash_at_risk = cash_at_risk

        self.alpaca_client = TradingClient(
            api_key=conf.alpaca_creds.api_key,
            secret_key=conf.alpaca_creds.secret_key.get_secret_value(),
            paper=conf.alpaca_creds.paper
        )

    def get_cash(self):

        account = self.alpaca_client.get_account()
        cash = float(account.buying_power)
        logger.debug(f"Available cash for trading (buying_power): {cash}")

        return cash

    def position_sizing(self, symbol):
        """
        Calculate the quantity of shares to buy based on the cash at risk

        Returns:
        --------
        quantity: int
            The number of shares to buy
        """

        cash = min(self.get_cash(), 500)

        last_price = self.get_last_price(symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)


        return cash, last_price, quantity


    def make_order(self, symbol, action):

        cash, last_price, quantity = self.position_sizing(symbol=symbol)

        if action == "buy":

            if quantity > 0:
                logger.debug(f"Position sizing: {quantity} shares of {symbol} at {last_price}")
                take_profit_price = round(last_price * 1.20, 2)
                stop_loss_price = round(last_price * .95, 2)

                order = self.create_order(
                    asset=symbol,
                    quantity=quantity,
                    time_in_force="day", # valid for today only
                    side="buy",
                    type="limit",
                    limit_price=last_price,
                    take_profit_price=take_profit_price,
                    stop_loss_price=stop_loss_price
                )
                logger.debug(f"Placing order: {order}")
                self.submit_order(order)
            else:
                logger.info(f"Insufficient cash to buy {symbol} at {last_price}, implied quantity: {quantity}")

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
                    logger.debug(f"Placing order: {order}")
                    self.submit_order(order)

            # cancel orders
            orders = self.alpaca_client.get_orders()
            for order in orders:
                if order.symbol == symbol:
                    logger.debug(f"Cancelling order: {order}")
                    self.cancel_order(order)
        else:
            logger.error(f"Invalid action: {action}")

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

    trader.make_order("AAPL", "buy")

    trader.make_order("AAPL", "sell")

    trader.make_order("TSLA", "sell")
