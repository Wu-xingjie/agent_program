from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_ollama.chat_models import ChatOllama


bailian_llm = ChatOpenAI(
    model = "qwen3-max",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key = SecretStr("sk-0447fbe1a6fb43d38cb83123bf7a0fd0"),
)

ollama_llm = ChatOllama(
    model = "qwen3.5:0.8b",
    temperature = 0.2
)
