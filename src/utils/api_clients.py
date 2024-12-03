# src/models/llm_provider.py

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

def get_llm(model_name='gpt-4', temperature=0.7):
    return ChatOpenAI(model_name=model_name, temperature=temperature)