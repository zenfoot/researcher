# src/models/llm_provider.py

# from langchain.chat_models import ChatOpenAI
# from langchain.llms import OpenAI

# def get_llm(model_name='gpt-4', temperature=0.7):
#     return ChatOpenAI(model_name=model_name, temperature=temperature)


import requests
import os
import backoff
import time

class SemanticScholarAPI:
    def __init__(self):
        self.api_key = os.getenv("S2_API_KEY")
        self.base_url = "https://api.semanticscholar.org/graph/v1"

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
    def search_papers(self, query, result_limit=10):
        if not query:
            return []
        response = requests.get(
            f"{self.base_url}/paper/search",
            headers={"X-API-KEY": self.api_key},
            params={
                "query": query,
                "limit": result_limit,
                "fields": "title,authors,venue,year,abstract,citationCount"
            }
        )
        response.raise_for_status()
        results = response.json()
        return results.get('data', [])