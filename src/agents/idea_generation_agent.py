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


from langchain.prompts import PromptTemplate
from models.llm_provider import get_llm
import json

class IdeaGenerationAgent:
    def __init__(self, task_description, code_snippet, prev_ideas, num_reflections):
        self.llm = get_llm()
        with open('src/prompts/idea_generation_prompt.txt', 'r') as f:
            self.idea_generation_prompt = f.read()
        self.task_description = task_description
        self.code_snippet = code_snippet
        self.prev_ideas_string = "\n\n".join(json.dumps(idea) for idea in prev_ideas)
        self.num_reflections = num_reflections

    def generate_idea(self):
        prompt = self.idea_generation_prompt.format(
            task_description=self.task_description,
            code=self.code_snippet,
            prev_ideas_string=self.prev_ideas_string,
            num_reflections=self.num_reflections
        )
        response = self.llm.predict(prompt)
        idea_json = self.extract_json(response)
        return idea_json, response

    def extract_json(self, text):
        # Logic to extract JSON between markers
        # For illustration, simplified extraction
        try:
            json_str = text.split('NEW IDEA JSON:\n```json')[1].split('```')[0].strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            return None


# from models.llm_provider import get_llm
# from prompts import load_prompt
# import json

# class IdeaGenerationAgent:
#     def __init__(self, domain, num_ideas=5):
#         self.llm = get_llm()
#         self.prompt_template = load_prompt('idea_generation_prompt.txt')
#         self.domain = domain
#         self.num_ideas = num_ideas

#     def generate_ideas(self):
#         prompt = self.prompt_template.format(domain=self.domain, num_ideas=self.num_ideas)
#         response = self.llm.predict(prompt)
#         ideas = self.parse_response(response)
#         return ideas

#     def parse_response(self, response):
#         # Implement parsing logic based on response format
#         return response.strip().split('\n')