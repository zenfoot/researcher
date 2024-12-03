"""
Generates innovative research ideas using language models.

This agent leverages LLMs to create novel and impactful research ideas
in a specified domain.
"""


from langchain.prompts import PromptTemplate
from models.llm_provider import get_llm

class IdeaGenerationAgent:
    def __init__(self):
        self.llm = get_llm()
        with open('src/prompts/idea_generation_prompt.txt', 'r') as f:
            self.prompt_template = f.read()

    def generate_ideas(self, domain, num_ideas=5):
        prompt = self.prompt_template.format(domain=domain, num_ideas=num_ideas)
        response = self.llm.predict(prompt)
        ideas = self.parse_ideas(response)
        return ideas

    def parse_ideas(self, response):
        # Implement parsing logic based on response format
        ideas = []
        for idea in response.split('\n'):
            if idea.strip():
                ideas.append(idea.strip())
        return ideas