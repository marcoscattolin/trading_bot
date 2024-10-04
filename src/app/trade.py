from src.libs.traders import AlpacaTrader
from src.libs.listeners import NewsListener
from src.libs.analysts import LLMAnalyst

class Analyst(LLMAnalyst):

    def __init__(self, trader):
        self.trader = trader
        super().__init__()

    def dispatch(self, message):
        self.trader.make_order(symbol=message["symbol"], action=message["action"])

class Listener(NewsListener):

    def __init__(self, symbols, analyst):
        self.analyst = analyst
        super().__init__(symbols=symbols)

    def dispatch(self, message):
        self.analyst.analyze(message)


if __name__ == "__main__":

    trader = AlpacaTrader()
    analyst = Analyst(trader=trader)
    listener = Listener(symbols=["*"], analyst=analyst)
    listener.run()
