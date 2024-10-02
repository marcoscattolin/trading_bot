from lumibot.strategies.strategy import Strategy
from src.utils.logging import logger
from src.config.config import conf
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from timedelta import Timedelta
from alpaca.data.timeframe import TimeFrame

class GoldenCross(Strategy):

    def initialize(self, symbol:str="AAPL", sleeptime:str="24H", short_window:int=7, long_window:int=14, cash_at_risk:float=.5):

        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.cash_at_risk = cash_at_risk
        self.sleeptime = sleeptime

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

        # Get the short and long moving averages
        short_mov_avg, long_mov_avg = self.get_moving_average()

        # If the short moving average is above the long moving average, buy
        if short_mov_avg > long_mov_avg:

            order = self.create_order(
                asset=self.symbol,
                quantity=quantity,
                side="buy",
                type="bracket",
                take_profit_price=last_price * 1.20,
                stop_loss_price=last_price * .95
            )

            self.submit_order(order)

        # If the short moving average is below the long moving average, sell
        elif short_mov_avg < long_mov_avg:
            # sell all
            self.sell_all()
        else:
            logger.info(f"Nothing to do")

    def get_moving_average(self):

        end = self.get_datetime()
        start = end - Timedelta(days=365) # last 365 prices

        stock_client = StockHistoricalDataClient(
            api_key=conf.alpaca_creds.api_key,
            secret_key=conf.alpaca_creds.secret_key.get_secret_value()
        )

        request_params = StockBarsRequest(
            symbol_or_symbols=[self.symbol],
            timeframe=TimeFrame.Day,
            start=start,
            end=end
        )
        bars = stock_client.get_stock_bars(request_params)
        prices = [x.open for x in bars.data[self.symbol]]

        short_mov_avg = sum(prices[-self.short_window:]) / self.short_window
        long_mov_avg = sum(prices[-self.long_window:]) / self.long_window

        return short_mov_avg, long_mov_avg