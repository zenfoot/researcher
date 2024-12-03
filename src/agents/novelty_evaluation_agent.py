"""
Evaluates the novelty of ideas against existing literature.

Using LLMs and external databases, this agent determines whether a research
idea is novel or has been previously explored.
"""


from agents.knowledge_management_agent import KnowledgeManagementAgent
from models.llm_provider import get_llm

class NoveltyEvaluationAgent:
    def __init__(self):
        self.llm = get_llm()
        self.km_agent = KnowledgeManagementAgent()

    def evaluate_novelty(self, idea):
        similar_docs = self.km_agent.query(idea)
        if not similar_docs:
            return True  # Novel idea
        # Further evaluation using LLM
        prompt = f"Assess the novelty of the following idea considering existing research:\nIdea: {idea}\nSimilar Research: {similar_docs}\nIs this idea novel? Yes or No. Provide justification."
        response = self.llm.predict(prompt)
        return "Yes" in response