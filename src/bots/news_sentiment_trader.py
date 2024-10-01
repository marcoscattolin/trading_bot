from lumibot.strategies.strategy import Strategy
from src.config.config import conf
from alpaca_trade_api import REST
from timedelta import Timedelta
import src.ml_utils.fin_bert as fin_bert

class NewsSentimentTrader(Strategy):

    name = "NewsSentimentTrader"

    def initialize(self, symbol:str, cash_at_risk:float, sleeptime:str, api_key:str, secret_key:str, base_url:str):

        self.symbol = symbol
        self.sleeptime = sleeptime
        self.last_trade = None
        self.api = REST(
            base_url=base_url,
            key_id=api_key,
            secret_key=secret_key
        )
        self.cash_at_risk = cash_at_risk

    def get_dates(self):

        today = self.get_datetime()
        three_days_ago = today - Timedelta(days=3)

        start = three_days_ago.strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")

        return start, end


    def get_sentiment(self):
        """
        Get the latest news for the symbol

        Returns:
        --------
        news: list
            A list of the latest news
        """
        start, end = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=start, end=end)

        news = [x.__dict__["_raw"]["headline"] for x in news]
        probability, sentiment = fin_bert.estimate_sentiment(news)
        return probability, sentiment


    def position_sizing(self):
        """
        Calculate the quantity of shares to buy based on the cash at risk

        Returns:
        --------
        quantity: int
            The number of shares to buy
        """
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)

        return cash, last_price, quantity


    def on_trading_iteration(self):

        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if cash > last_price:

            if sentiment == "positive" and probability > .999:
                if self.last_trade == "sell":
                    self.sell_all()

                order = self.create_order(
                    asset=self.symbol,
                    quantity=quantity,
                    side="buy",
                    type="bracket",
                    take_profit_price=last_price * 1.20,
                    stop_loss_price=last_price * .95
                )
                self.submit_order(order)
                self.last_trade = "buy"

            elif sentiment == "negative" and probability > .999:
                if self.last_trade == "buy":
                    self.sell_all()

                order = self.create_order(
                    asset=self.symbol,
                    quantity=quantity,
                    side="sell",
                    type="bracket",
                    take_profit_price=last_price * 0.8,
                    stop_loss_price=last_price * 1.05
                )
                self.submit_order(order)
                self.last_trade = "sell"
