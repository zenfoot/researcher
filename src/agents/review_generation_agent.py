"""
Generates peer reviews using language models.

The agent creates detailed reviews of the research paper, highlighting
strengths, weaknesses, and suggestions for improvement.
"""


import json
from models.llm_provider import get_llm
from prompts import (
    load_prompt,
    load_reviewer_system_prompt_base,
    load_reviewer_system_prompt_neg,
    load_reviewer_system_prompt_pos,
)
from utils.paper_loader import PaperLoader
from utils.few_shot_examples import get_review_fewshot_examples

class ReviewGenerationAgent:
    def __init__(
        self,
        model_name='gpt-4',
        temperature=0.7,
        num_reflections=1,
        num_fs_examples=1,
        num_reviews_ensemble=1,
        reviewer_system_prompt='neg',  # 'base', 'neg', or 'pos'
        client=None,
    ):
        self.llm = get_llm(model_name=model_name, temperature=temperature)
        self.num_reflections = num_reflections
        self.num_fs_examples = num_fs_examples
        self.num_reviews_ensemble = num_reviews_ensemble
        self.reviewer_system_prompt = self.load_system_prompt(reviewer_system_prompt)
        self.client = client  # For API rate limiting, etc.

    def load_system_prompt(self, prompt_type):
        if prompt_type == 'base':
            return load_reviewer_system_prompt_base()
        elif prompt_type == 'neg':
            return load_reviewer_system_prompt_neg()
        elif prompt_type == 'pos':
            return load_reviewer_system_prompt_pos()
        else:
            return load_reviewer_system_prompt_neg()

    def perform_review(self, paper_text):
        # Load prompts
        template_instructions = load_prompt('template_instructions.txt')
        neurips_form = load_prompt('neurips_form_instructions.txt') + template_instructions

        # Few-shot examples
        if self.num_fs_examples > 0:
            fs_prompt = get_review_fewshot_examples(self.num_fs_examples)
            base_prompt = neurips_form + fs_prompt
        else:
            base_prompt = neurips_form
        base_prompt += f"\nHere is the paper you are asked to review:\n```{paper_text}```"

        # Generate initial review(s)
        if self.num_reviews_ensemble > 1:
            reviews = self.generate_ensemble_reviews(base_prompt)
            review = self.aggregate_reviews(reviews)
        else:
            review = self.generate_single_review(base_prompt)

        # Reflection and refinement
        if self.num_reflections > 1:
            review = self.reflect_on_review(review)

        return review

    def generate_single_review(self, prompt):
        response = self.llm.predict(prompt, system_message=self.reviewer_system_prompt)
        review = self.extract_json_between_markers(response)
        return review

    def generate_ensemble_reviews(self, prompt):
        responses = self.llm.generate(
            [prompt] * self.num_reviews_ensemble,
            system_message=self.reviewer_system_prompt,
            n=self.num_reviews_ensemble,
            stop=None,
        )
        reviews = []
        for response in responses:
            review = self.extract_json_between_markers(response)
            if review:
                reviews.append(review)
        return reviews

    def aggregate_reviews(self, reviews):
        # Meta-review agent to aggregate reviews
        meta_review_agent = MetaReviewAgent()
        aggregated_review = meta_review_agent.aggregate_reviews(reviews)
        return aggregated_review

    def reflect_on_review(self, review):
        reflection_agent = ReviewReflectionAgent()
        for current_round in range(1, self.num_reflections + 1):
            review = reflection_agent.reflect(review, current_round, self.num_reflections)
            if 'I am done' in review.get('THOUGHT', ''):
                break
        return review

    @staticmethod
    def extract_json_between_markers(text):
        # Implement logic to extract JSON between markers
        try:
            json_str = text.split('REVIEW JSON:\n```json')[1].split('```')[0].strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            return None