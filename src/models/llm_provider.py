"""
Provides interfaces to access language models (LLMs).

This module abstracts the interaction with LLMs, facilitating
uniform access and model switching if necessary.
"""


from langchain.chat_models import ChatOpenAI

def get_llm(model_name='gpt-4', temperature=0.7):
    return ChatOpenAI(model_name=model_name, temperature=temperature)