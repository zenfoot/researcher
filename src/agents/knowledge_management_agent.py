"""
Manages knowledge resources and information retrieval.

This agent handles the acquisition, storage, and retrieval of knowledge
necessary for informed decision-making by other agents.
"""


from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class KnowledgeManagementAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma("knowledge_base", self.embeddings)

    def add_document(self, document):
        self.vectorstore.add_texts([document])

    def query(self, query, top_k=5):
        return self.vectorstore.similarity_search(query, k=top_k)