from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="deepseek-v2",
    temperature=0.7,
    )
from langchain_core.messages import AIMessage

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
ai_msg