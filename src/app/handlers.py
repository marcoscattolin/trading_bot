from abc import abstractmethod

from Tools.scripts.nm2def import symbols
from langchain_openai import ChatOpenAI
from src.config.config import conf
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import asyncio
from src.utils.logging import logger
from lumibot.brokers import Alpaca
from src.app.traders import AlpacaTrader

class DebugData:

    def __init__(self, symbols, headline, summary):
        self.symbols = symbols
        self.headline = headline
        self.summary = summary

    def __str__(self):
        return f"Symbols: {self.symbols}, Headline: {self.headline}, Summary: {self.summary}"

class Handler:

    def get_handler(self):
        return self._handler

    @abstractmethod
    async def _handler(self, data):
        pass

class PrinterHandler(Handler):

    # async handler
    async def _handler(self, data):
        logger.debug(data)


class LLMHandler(Handler):

    def __init__(self):

        chat = ChatOpenAI(
            openai_api_key=conf.openai.api_key.get_secret_value(),
            model="gpt-4o",
            temperature=0.2
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a seasoned financial advisor expert in trading Stocks. You are here to suggest the "
                    "best stocks to buy or sell depending on the latest news. When the user sends a message, you should "
                    "reply with the best stock to buy based on the latest news. When you reply, just use the stock "
                    "symbol, the action (buy/sell) and the reason why you suggest that action. Use '-' to separate the "
                    "stock symbol, the action and the reason.  For example: AAPL - buy - reason. If the message is not "
                    "relevant for trading stocks, just reply with '<not_relevant>'.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        self.chain = prompt | chat

    def _parse_data(self, data):

        # extract symbols from the data
        symbols = ", ".join(data.symbols)
        headline = data.headline
        summary = data.summary
        message = f"{symbols} | {headline} | {summary} | "
        logger.warning(f"NEWS: {message}")

        try:
            result = self.chain.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=message
                        )
                    ]
                }
            )
            logger.warning(f"LLM: {result.content}")

            # parse the result
            if result.content == "<not_relevant>":
                return "<not_relevant>", "<not_relevant>", "<not_relevant>"
            else:
                symbol, action, reason = result.content.split(" - ")
                return symbol, action, reason
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return "<not_relevant>", "<not_relevant>", "<not_relevant>"

    # async handler
    async def _handler(self, data):
        symbol, action, reason = self._parse_data(data)
        return symbol, action, reason



class LLMTradingHandler(LLMHandler):

    def __init__(self):

        # call super
        super().__init__()

        # init broker
        alpaca_config = {
            "API_KEY": conf.alpaca_creds.api_key,
            "API_SECRET": conf.alpaca_creds.secret_key.get_secret_value(),
            "PAPER": conf.alpaca_creds.paper,
        }
        broker = Alpaca(alpaca_config)

        self.trader = AlpacaTrader(broker=broker)

        self.trader.initialize()

    # async handler
    async def _handler(self, data):

        symbol, action, reason = self._parse_data(data)
        if symbol == "<not_relevant>":
            pass
        elif action not in ["buy", "sell"]:
            pass
        else:
            self.trader.make_order(symbol, action)


if __name__ == "__main__":

    async def main():
        handler = LLMHandler().get_handler()

        data = {
            "symbols": ["AAPL", "NVDA"],
            "headline": "Apple shares are expected to boom in the following days.",
            "summary": "Apple is expected to release a new product that will revolutionize the industry."
        }

        symbol, action, reason = await handler(DebugData(**data))
        print(symbol, action, reason)

        data = {
            "symbols": ["AAPL", "NVDA"],
            "headline": "Nvidia is declaring bankruptcy.",
            "summary": "Nvidia is facing financial difficulties and is expected to declare bankruptcy."
        }
        symbol, action, reason = await handler(DebugData(**data))
        print(symbol, action, reason)

        data = {
            "symbols": ["AAPL", "NVDA"],
            "headline": "What is the secret to happiness?",
            "summary": "The secret"
        }
        symbol, action, reason = await handler(DebugData(**data))
        print(symbol, action, reason)

    asyncio.run(main())
