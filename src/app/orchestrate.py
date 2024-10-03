from src.app.handlers import LLMHandler
from src.app.listeners import NewsListener
from src.app.traders import AlpacaTrader



def run():

    handler = LLMHandler().get_handler()
    listener = NewsListener(handler, symbols=["*"])
    listener.run()


if __name__ == "__main__":
    run()

