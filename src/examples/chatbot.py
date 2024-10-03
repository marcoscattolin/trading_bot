from langchain_openai import ChatOpenAI
from src.config.config import conf
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def initialize_chat():
    chat = ChatOpenAI(
        openai_api_key=conf.openai.api_key.get_secret_value(),
        model="gpt-4o",
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful italian assistant. Answer all questions in italian, disregarding the language in which the question was made.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt | chat

def main():
    chain = initialize_chat()

    try:
        result = chain.invoke(
            {
                "messages": [
                    HumanMessage(
                        content="What is the secret to happiness?"
                    )
                ]
            }
        )
        print(result.content)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()