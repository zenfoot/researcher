"""
Refines reviews through iterative self-reflection.

This agent enhances the initial reviews by reflecting on the feedback,
making them more constructive and thorough.
"""


import json
from models.llm_provider import get_llm
from prompts import load_prompt

class ReviewReflectionAgent:
    def __init__(self, model_name='gpt-4', temperature=0.7):
        self.llm = get_llm(model_name=model_name, temperature=temperature)
        self.reviewer_reflection_prompt = load_prompt('reviewer_reflection_prompt.txt')
        self.reviewer_system_prompt = load_prompt('reviewer_system_prompt_neg.txt')  # Or load as needed

    def reflect(self, review, current_round, num_reflections):
        prompt = self.reviewer_reflection_prompt.format(current_round=current_round, num_reflections=num_reflections)
        prompt += f"\nHere is the review you just created:\n```json\n{json.dumps(review)}\n```"
        response = self.llm.predict(prompt, system_message=self.reviewer_system_prompt)
        return self.extract_json_between_markers(response)

    @staticmethod
    def extract_json_between_markers(text):
        # Implement logic to extract JSON between markers
        try:
            json_str = text.split('REVIEW JSON:\n```json')[1].split('```')[0].strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            return None