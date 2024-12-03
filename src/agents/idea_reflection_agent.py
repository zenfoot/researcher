"""
Refines and improves generated ideas through reflection.

The agent reviews initial ideas, enhancing them by identifying potential
improvements and increasing their novelty and feasibility.
"""


from langchain.prompts import PromptTemplate
from models.llm_provider import get_llm
import json

class IdeaReflectionAgent:
    def __init__(self, idea_json, current_round, num_reflections):
        self.llm = get_llm()
        with open('src/prompts/idea_reflection_prompt.txt', 'r') as f:
            self.idea_reflection_prompt = f.read()
        self.idea_json = idea_json
        self.current_round = current_round
        self.num_reflections = num_reflections

    def reflect_on_idea(self, msg_history):
        prompt = self.idea_reflection_prompt.format(
            current_round=self.current_round,
            num_reflections=self.num_reflections
        )
        response = self.llm.predict(prompt, chat_history=msg_history)
        idea_json = self.extract_json(response)
        return idea_json, response

    def extract_json(self, text):
        # Logic to extract JSON between markers
        try:
            json_str = text.split('NEW IDEA JSON:\n```json')[1].split('```')[0].strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            return None