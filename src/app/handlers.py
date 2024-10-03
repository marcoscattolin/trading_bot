from abc import abstractmethod
from langchain_openai import ChatOpenAI
from src.config.config import conf
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import asyncio


class Handler:

    def get_handler(self):
        return self._handler

    @abstractmethod
    async def _handler(self, data):
        pass

class PrinterHandler(Handler):

    # async handler
    async def _handler(self, data):
        print(data)


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


    # async handler
    async def _handler(self, data):
        print(data)
        try:
            result = self.chain.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=data
                        )
                    ]
                }
            )

            # parse the result
            if result.content == "<not_relevant>":
                return "<not_relevant>", "<not_relevant>", "<not_relevant>"
            else:
                symbol, action, reason = result.content.split(" - ")
                return symbol, action, reason
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    async def main():
        handler = LLMHandler().get_handler()

        symbol, action, reason = await handler("Apple shares are expected to boom in the following days.")
        print(symbol, action, reason)

        symbol, action, reason = await handler("Nvidia is declaring bankruptcy.")
        print(symbol, action, reason)

        symbol, action, reason = await handler("What is the secret to happiness?")
        print(symbol, action, reason)

    asyncio.run(main())
