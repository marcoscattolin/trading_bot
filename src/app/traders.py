from lumibot.strategies.strategy import Strategy
from src.config.config import conf
from src.utils.logging import logger
from lumibot.brokers import Alpaca
from alpaca.trading.client import TradingClient

class LLMTrader(Strategy):

    def initialize(self, cash_at_risk:float = 0.5):

        self.cash_at_risk = cash_at_risk

        self.alpaca_client = TradingClient(
            api_key=conf.alpaca_creds.api_key,
            secret_key=conf.alpaca_creds.secret_key.get_secret_value(),
            paper=conf.alpaca_creds.paper
        )

    def get_cash(self):

        account = self.alpaca_client.get_account()
        return float(account.cash)

    def position_sizing(self, symbol):
        """
        Calculate the quantity of shares to buy based on the cash at risk

        Returns:
        --------
        quantity: int
            The number of shares to buy
        """
        cash = self.get_cash()

        last_price = self.get_last_price(symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)

        return cash, last_price, quantity


    def make_order(self, symbol, action):

        cash, last_price, quantity = self.position_sizing(symbol=symbol)

        if action == "buy":

            if quantity > 0:

                take_profit_price = round(last_price * 1.20, 2)
                stop_loss_price = round(last_price * .95, 2)

                order = self.create_order(
                    asset=symbol,
                    quantity=quantity,
                    side="buy",
                    type="bracket",
                    take_profit_price=take_profit_price,
                    stop_loss_price=stop_loss_price
                )
                self.submit_order(order)
            else:
                logger.info(f"Insufficient cash to buy {symbol}")

        elif action == "sell":
            # close positions
            position = self.get_position(symbol)
            if position:
                order = self.create_order(
                    asset=symbol,
                    quantity=position.quantity,
                    side="sell",
                    type="market"
                )
                self.submit_order(order)

            # cancel orders
            orders = self.get_orders()
            for order in orders:
                if order.symbol == symbol:
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

    trader = LLMTrader(broker=broker)

    trader.initialize()

    trader.make_order("AAPL", "buy")

    trader.make_order("AAPL", "sell")

    trader.make_order("TSLA", "sell")
