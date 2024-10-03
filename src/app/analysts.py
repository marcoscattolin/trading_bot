from abc import abstractmethod
from langchain_openai import ChatOpenAI
from src.config.config import conf
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import asyncio
from src.utils.logging import logger
from lumibot.brokers import Alpaca
from src.app.traders import AlpacaTrader

class LLMAnalyst:

    name = "LLMAnalyst"

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

    @abstractmethod
    def _format_input(self, message):

        logger.debug(f"[{self.name}]: Parsing message: {message}")

        # extract symbols from the data
        symbols = ", ".join(message.get("symbols"))
        headline = message.get("headline")
        summary = message.get("summary")
        message = f"{symbols} | {headline} | {summary} | "

        return message

    def _format_output(self, llm_output):

        logger.debug(f"[{self.name}]: Parsing llm output: {llm_output}")
        # parse the result
        if llm_output == "<not_relevant>":
            return None
        else:

            symbol, action, reason = llm_output.content.split(" - ")
            if action not in ["buy", "sell"]:
                return None
            else:
                output_message = {
                    "symbol": symbol,
                    "action": action,
                    "reason": reason,
                }

            return output_message

    def analyze(self, message):

        try:
            result = self.chain.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=self._format_input(message)
                        )
                    ]
                }
            )

            message = self._format_output(result)
            if message:
                self.dispatch(message)

        except:
            # do nothing
            return None

    def dispatch(self, message):

        # to be customized in inherited classes
        logger.debug(f"[{self.name}] will dispatch message: {message}")


if __name__ == "__main__":

    analyst = LLMAnalyst()

    data = [
        {
            "symbols": ["AAPL", "NVDA"],
            "headline": "Apple shares are expected to boom in the following days.",
            "summary": "Apple is expected to release a new product that will revolutionize the industry."
        },
        {
            "symbols": ["AAPL", "NVDA"],
            "headline": "Nvidia is declaring bankruptcy.",
            "summary": "Nvidia is facing financial difficulties and is expected to declare bankruptcy."
        },
        {
            "symbols": ["AAPL", "NVDA"],
            "headline": "What is the secret to happiness?",
            "summary": "The secret"
        }
        ]

    for d in data:
        analyst.analyze(d)
