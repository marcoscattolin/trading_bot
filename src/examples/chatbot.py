from langchain_openai import ChatOpenAI
from src.config.config import conf
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


chat = ChatOpenAI(
    openai_api_key=conf.openai.api_key.get_secret_value(),
    model="gpt-4o",
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful italain assistant. Answer all questions in italian, disregarding the language in which the question was made.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | chat

result = chain.invoke(
    [
        HumanMessage(
            content="What is the secret to happiness?"
        )
    ]
)
print(result.content)
