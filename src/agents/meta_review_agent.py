"""
Aggregates multiple reviews into a cohesive meta-review.

The agent combines feedback from several reviews to form a single,
comprehensive meta-review summarizing essential points.
"""


import json
import numpy as np
from models.llm_provider import get_llm
from prompts import load_prompt

class MetaReviewAgent:
    def __init__(self, model_name='gpt-4', temperature=0.7):
        self.llm = get_llm(model_name=model_name, temperature=temperature)
        self.meta_reviewer_system_prompt = load_prompt('meta_reviewer_system_prompt.txt')
        self.neurips_form = load_prompt('neurips_form_instructions.txt')

    def aggregate_reviews(self, reviews):
        review_text = ""
        for i, r in enumerate(reviews):
            review_text += f"""Review {i + 1}/{len(reviews)}:\n```{json.dumps(r)}\n```\n"""
        base_prompt = self.neurips_form + "\n" + review_text

        response = self.llm.predict(base_prompt, system_message=self.meta_reviewer_system_prompt.format(reviewer_count=len(reviews)))
        aggregated_review = self.extract_json_between_markers(response)
        return aggregated_review

    @staticmethod
    def extract_json_between_markers(text):
        # Implement logic to extract JSON between markers
        try:
            json_str = text.split('REVIEW JSON:\n```json')[1].split('```')[0].strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            return None