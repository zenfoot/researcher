"""
Plans experiments to test the selected research idea.

The agent outlines the experimental approach, defining objectives,
methodologies, and required resources.
"""


from langchain.prompts import PromptTemplate
from models.llm_provider import get_llm
import os

class ExperimentPlanningAgent:
    def __init__(self, idea_title, idea_description, max_runs, baseline_results):
        self.llm = get_llm()
        with open('src/prompts/coder_prompt.txt', 'r') as f:
            self.coder_prompt_template = f.read()
        self.idea_title = idea_title
        self.idea_description = idea_description
        self.max_runs = max_runs
        self.baseline_results = baseline_results
        self.experiment_plan = []

    def plan_experiments(self):
        prompt = self.coder_prompt_template.format(
            title=self.idea_title,
            idea=self.idea_description,
            max_runs=self.max_runs,
            baseline_results=self.baseline_results
        )
        response = self.llm.predict(prompt)
        # Extract experiment plan from response
        self.experiment_plan = self.parse_experiment_plan(response)
        return response

    def parse_experiment_plan(self, response):
        # Implement parsing logic to extract the experiment plan
        # For illustration, assume the LLM outputs a list of experiments
        experiments = []
        # Parsing logic to populate the experiments list based on response
        return experiments