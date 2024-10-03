from abc import abstractmethod
from langchain_openai import ChatOpenAI
from src.config.config import conf
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


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

        self.chat = ChatOpenAI(
            openai_api_key=conf.openai.api_key.get_secret_value(),
            model="gpt-4o",
            temperature=0.2
        )

        self.prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )



    # async handler
    async def _handler(self, data):
        print(data)